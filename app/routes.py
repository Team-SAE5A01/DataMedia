from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes pour MySQL (Utilisateurs)
@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Routes pour MongoDB (Trajets)
@router.post("/trajets/")
def create_trajet(trajet: schemas.TrajetBase):
    collection = database.mongo_db["trajets"]
    return {"id": crud.create_trajet(collection, trajet)}

@router.get("/trajets/{user_id}")
def get_trajet(user_id: int):
    collection = database.mongo_db["trajets"]
    trajet = crud.get_trajet(collection, user_id)
    if trajet is None:
        raise HTTPException(status_code=404, detail="Trajet not found")
    trajet["_id"] = str(trajet["_id"])  # Convertir ObjectId en string
    return trajet

@router.get("/test")
def get_trajet():
    return "Hello world"