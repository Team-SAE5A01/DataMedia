from sqlalchemy.orm import Session
from src.db.models.bagage_models import Bagage
from src.db.schemas.bagage_schemas import BagageBase, BagageUpdate

def create_bagage(db: Session, bagage: BagageBase):
    """
    Crée un nouveau bagage et l'ajoute à la base de données.
    """
    db_bagage = Bagage(**bagage.dict())
    db.add(db_bagage)
    db.commit()
    db.refresh(db_bagage)
    return db_bagage

def get_bagage(db: Session, bagage_id: int):
    """
    Récupère un bagage par son ID.
    """
    return db.query(Bagage).filter(Bagage.id == bagage_id).first()

def get_bagages_by_user(db: Session, user_id: int):
    """
    Récupère tous les bagages d'un utilisateur.
    """
    return db.query(Bagage).filter(Bagage.user_id == user_id).all()

def update_bagage(db: Session, bagage_id: int, bagage_update: BagageUpdate):
    """
    Met à jour un bagage existant.
    """
    db_bagage = get_bagage(db, bagage_id)
    if not db_bagage:
        return None
    
    update_data = bagage_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_bagage, key, value)

    db.commit()
    db.refresh(db_bagage)
    return db_bagage

def delete_bagage(db: Session, bagage_id: int):
    """
    Supprime un bagage de la base de données.
    """
    db_bagage = get_bagage(db, bagage_id)
    if not db_bagage:
        return None
    
    db.delete(db_bagage)
    db.commit()
    return db_bagage
