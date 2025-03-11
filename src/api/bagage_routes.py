from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.crud import bagage_crud
from src.db.schemas.bagage_schemas import BagageBase, BagageResponse, BagageUpdate
from src.db.models.bagage_models import Bagage
from src.core import config

router = APIRouter(tags=["Bagages"])

def get_db():
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route pour ajouter un bagage
@router.post("/bagages/", response_model=BagageResponse)
def create_bagage(bagage: BagageBase, db: Session = Depends(get_db)):
    db_bagage = Bagage(**bagage.dict())
    db.add(db_bagage)
    db.commit()
    db.refresh(db_bagage)
    return db_bagage

# Route pour récupérer un bagage par ID
@router.get("/bagages/{bagage_id}", response_model=BagageResponse)
def get_bagage(bagage_id: int, db: Session = Depends(get_db)):
    db_bagage = db.query(Bagage).filter(Bagage.id == bagage_id).first()
    if db_bagage is None:
        raise HTTPException(status_code=404, detail="Bagage non trouvé")
    return db_bagage

# Route pour récupérer tous les bagages d'un utilisateur
@router.get("/users/{user_id}/bagages/", response_model=list[BagageResponse])
def get_bagages_by_user(user_id: int, db: Session = Depends(get_db)):
    db_bagages = db.query(Bagage).filter(Bagage.user_id == user_id).all()
    return db_bagages

# Route pour mettre à jour un bagage
@router.put("/bagages/{bagage_id}", response_model=BagageResponse)
def update_bagage(bagage_id: int, bagage: BagageUpdate, db: Session = Depends(get_db)):
    updated_bagage = bagage_crud.update_bagage(db, bagage_id, bagage)
    if not updated_bagage:
        raise HTTPException(status_code=404, detail="Bagage not found")
    return updated_bagage

# Route pour supprimer un bagage
@router.delete("/bagages/{bagage_id}")
def delete_bagage(bagage_id: int, db: Session = Depends(get_db)):
    db_bagage = db.query(Bagage).filter(Bagage.id == bagage_id).first()
    if db_bagage is None:
        raise HTTPException(status_code=404, detail="Bagage non trouvé")
    
    db.delete(db_bagage)
    db.commit()
    return {"message": "Bagage supprimé avec succès"}
