from fastapi import APIRouter, HTTPException

from src.db.schemas.voyage_schemas import VoyageBase
from src.core import config
from src.db.crud import user_crud

router = APIRouter()

def get_db():
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes pour MongoDB (Trajets)
@router.post("/trajets/")
def create_trajet(trajet: VoyageBase):
    collection = config.mongo_db["trajets"]
    return {"id": user_crud.create_trajet(collection, trajet)}

@router.get("/trajets/{user_id}")
def get_trajet(user_id: int):
    collection = config.mongo_db["trajets"]
    trajet = user_crud.get_trajet(collection, user_id)
    if trajet is None:
        raise HTTPException(status_code=404, detail="Trajet not found")
    trajet["_id"] = str(trajet["_id"])  # Convertir ObjectId en string
    return trajet