from sqlalchemy.orm import Session
from pymongo.collection import Collection

from app.db import schemas
from app.db import models

# CRUD pour MongoDB
def create_trajet(collection: Collection, trajet: models.TrajetBase):
    result = collection.insert_one(trajet.dict())
    return str(result.inserted_id)

def get_trajet(collection: Collection, user_id: int):
    return collection.find_one({"idUser": user_id})