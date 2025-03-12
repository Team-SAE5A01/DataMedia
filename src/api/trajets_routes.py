from fastapi import APIRouter, HTTPException
import json

router = APIRouter(tags=["Trajets"])

# Load JSON test data
test_data = json.loads("""
[
  {
    "trip_id": "trip-001",
    "client_id": "36",
    "origin": "City A",
    "destination": "City B",
    "status": "planned",
    "created_at": "2025-03-10T10:00:00Z",
    "updated_at": "2025-03-10T12:30:00Z",
    "steps": [
      {
        "step_id": "step-001a",
        "trip_id": "trip-001",
        "mode": "bus",
        "from": "Station A",
        "to": "Station B",
        "departure_time": "2025-03-11T08:00:00Z",
        "arrival_time": "2025-03-11T09:30:00Z",
        "assistant": {
          "assistant_id": "38",
          "name": "test test",
          "status": "assigned"
        }
      },
      {
        "step_id": "step-001b",
        "trip_id": "trip-001",
        "mode": "train",
        "from": "Station B",
        "to": "City B Central",
        "departure_time": "2025-03-11T10:00:00Z",
        "arrival_time": "2025-03-11T12:00:00Z",
        "assistant": {
          "assistant_id": "38",
          "name": "test test",
          "status": "assigned"
        }
      }
    ]
  },
  {
    "trip_id": "trip-002",
    "client_id": "36",
    "origin": "City C",
    "destination": "City D",
    "status": "ongoing",
    "created_at": "2025-03-09T11:00:00Z",
    "updated_at": "2025-03-10T13:45:00Z",
    "steps": [
      {
        "step_id": "step-002a",
        "trip_id": "trip-002",
        "mode": "plane",
        "from": "Airport C",
        "to": "Airport D",
        "departure_time": "2025-03-10T15:00:00Z",
        "arrival_time": "2025-03-10T18:30:00Z",
        "assistant": {
          "assistant_id": "38",
          "name": "test test",
          "status": "assigned"
        }
      }
    ]
  },
  {
    "trip_id": "trip-003",
    "client_id": "36",
    "origin": "City E",
    "destination": "City F",
    "status": "completed",
    "created_at": "2025-02-20T14:00:00Z",
    "updated_at": "2025-02-22T18:00:00Z",
    "steps": [
      {
        "step_id": "step-003a",
        "trip_id": "trip-003",
        "mode": "train",
        "from": "Station E",
        "to": "Station F",
        "departure_time": "2025-02-21T08:00:00Z",
        "arrival_time": "2025-02-21T11:30:00Z",
        "assistant": {
          "assistant_id": "38",
          "name": "test test",
          "status": "assigned"
        }
      },
      {
        "step_id": "step-003b",
        "trip_id": "trip-003",
        "mode": "taxi",
        "from": "Station F",
        "to": "Hotel F",
        "departure_time": "2025-02-21T12:00:00Z",
        "arrival_time": "2025-02-21T12:30:00Z",
        "assistant": {
          "assistant_id": "38",
          "name": "test test",
          "status": "assigned"
        }
      }
    ]
  }
]
""")


# USER ID = 36
# ASSISTANT ID = 38
# TRIPS : trip-001, trip-002, trip-003
@router.get("/trajets/user/{user_id}")
def get_user_trajets(user_id: str):
    """
    Fetch all trips for a specific user (client_id).
    """
    user_trips = [trip for trip in test_data if trip["client_id"] == user_id]

    if not user_trips:
        raise HTTPException(status_code=404, detail="No trips found for this user.")

    return user_trips


@router.get("/trajets/{trajet_id}")
def get_trajet(trajet_id: str):
    """
    Fetch a specific trip by its trip_id.
    """
    trip = next((trip for trip in test_data if trip["trip_id"] == trajet_id), None)

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found.")

    return trip

@router.get("/trajets")
def get_all_trajets():
    """
    Fetch all trips.
    """
    if not test_data:
        raise HTTPException(status_code=404, detail="No trips found.")

    return test_data
