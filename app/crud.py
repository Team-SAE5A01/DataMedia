from sqlalchemy.orm import Session
from pymongo.collection import Collection
from . import config, models, schemas

# CRUD pour MySQL
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
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
    return db.query(models.User).filter(models.User.id == user_id).first()

# CRUD pour MongoDB
def create_trajet(collection: Collection, trajet: schemas.TrajetBase):
    result = collection.insert_one(trajet.dict())
    return str(result.inserted_id)

def get_trajet(collection: Collection, user_id: int):
    return collection.find_one({"idUser": user_id})
