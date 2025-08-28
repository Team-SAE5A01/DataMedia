from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import uuid
import requests
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

SNCF_API_BASE = "https://api.sncf.com/v1/coverage/sncf"
SNCF_API_KEY = "da5d94c7-b58f-41b7-8012-b203a43724a7"
HEADERS = {"Authorization": SNCF_API_KEY, "Accept": "application/json"}

router = APIRouter(tags=["Itinéraires"])

# -------------------
# Pydantic Models
# -------------------
class Assistant(BaseModel):
    assistant_id: str = "38"
    name: str = "test test"
    status: str = "assigned"

class Step(BaseModel):
    step_id: str
    trip_id: str
    mode: str
    from_: str = Field(..., alias="from")
    to: str = Field(..., alias="to")
    departure_time: str
    arrival_time: str
    assistant: Assistant = Assistant()

class Trip(BaseModel):
    trip_id: str
    client_id: str = "36"
    origin: str
    destination: str
    status: str = "planned"
    created_at: str
    updated_at: str
    steps: List[Step]

# -------------------
# Helper functions
# -------------------
def search_station(query: str) -> Optional[Dict[str, Any]]:
    query = query.strip('"\'').strip()
    if not query:
        return None

    MAJOR_STATIONS = {
        'paris': {'id': 'stop_area:SNCF:87686006', 'name': 'Paris Gare de Lyon'},
        'lyon': {'id': 'stop_area:SNCF:87722025', 'name': 'Lyon Part-Dieu'},
        'marseille': {'id': 'stop_area:SNCF:87751008', 'name': 'Marseille Saint-Charles'},
    }
    query_lower = query.lower()
    if query_lower in MAJOR_STATIONS:
        station = MAJOR_STATIONS[query_lower]
        return {'id': station['id'], 'name': station['name'], 'stop_area': {'name': station['name']}}

    try:
        url = f"{SNCF_API_BASE}/places"
        params = {"q": query, "type[]": ["stop_area"], "count": 10, "depth": 2}
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        if not data.get('places'):
            return None
        for place in data['places']:
            if place.get('embedded_type') == 'stop_area':
                return {'id': place['id'], 'name': place.get('name', 'Gare inconnue')}
    except requests.exceptions.RequestException:
        return None

def get_journey(from_station: str, to_station: str) -> Optional[Dict[str, Any]]:
    from_place = search_station(from_station)
    to_place = search_station(to_station)
    if not from_place or not to_place or from_place['id'] == to_place['id']:
        return None

    url = f"{SNCF_API_BASE}/journeys"
    params = {
        "from": from_place['id'],
        "to": to_place['id'],
        "count": 1,
        "forbidden_uris[]": ["physical_mode:Bus", "physical_mode:Walking"],
        "data_freshness": "realtime",
        "_override_scenario": "new_default"
    }
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=20)
        data = response.json()
        if response.status_code != 200 or not data.get('journeys'):
            return None
        data['from_place'] = from_place
        data['to_place'] = to_place
        return data
    except requests.exceptions.RequestException:
        return None

def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# -------------------
# Routes
# -------------------
@router.get("/journeys", response_model=List[Trip])
async def get_journey_endpoint(from_station: str = Query(...), to_station: str = Query(...)):
    journey_data = get_journey(from_station, to_station)
    if not journey_data:
        raise HTTPException(status_code=404, detail="Aucun itinéraire trouvé entre ces gares")

    from_place_name = journey_data['from_place']['name']
    to_place_name = journey_data['to_place']['name']
    created_at = updated_at = iso_utc_now()
    trip_id = f"trip-{uuid.uuid4().hex[:8]}"

    steps = []
    for section in journey_data['journeys'][0].get('sections', []):
        step_id = f"step-{uuid.uuid4().hex[:8]}"
        step_data = {
            "step_id": step_id,
            "trip_id": trip_id,
            "mode": section.get('display_informations', {}).get('commercial_mode', section.get('type', 'unknown')).lower(),
            "from": section.get('from', {}).get('name', ''),
            "to": section.get('to', {}).get('name', ''),
            "departure_time": datetime.fromisoformat(section['departure_date_time']).isoformat().replace("+00:00", "Z"),
            "arrival_time": datetime.fromisoformat(section['arrival_date_time']).isoformat().replace("+00:00", "Z")
        }
        steps.append(Step(**step_data))

    trip = Trip(
        trip_id=trip_id,
        origin=from_place_name,
        destination=to_place_name,
        created_at=created_at,
        updated_at=updated_at,
        steps=steps
    )

    return [trip]
