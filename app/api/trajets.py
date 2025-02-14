from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import schemas
from app.core import config
from app.db.crud import users

router = APIRouter()

def get_db():
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes pour MongoDB (Trajets)
@router.post("/trajets/")
def create_trajet(trajet: schemas.TrajetBase):
    collection = config.mongo_db["trajets"]
    return {"id": users.create_trajet(collection, trajet)}

@router.get("/trajets/{user_id}")
def get_trajet(user_id: int):
    collection = config.mongo_db["trajets"]
    trajet = users.get_trajet(collection, user_id)
    if trajet is None:
        raise HTTPException(status_code=404, detail="Trajet not found")
    trajet["_id"] = str(trajet["_id"])  # Convertir ObjectId en string
    return trajet