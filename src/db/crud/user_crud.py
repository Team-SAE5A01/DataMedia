from sqlalchemy.orm import Session

from src.db.models.user_models import User
from src.db.schemas.user_schemas import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate):
    db_user = user.User(
        nom=user.nom,
        prenom=user.prenom,
        date_de_naissance=user.date_de_naissance,
        email=user.email,
        mot_de_passe=user.mot_de_passe,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user