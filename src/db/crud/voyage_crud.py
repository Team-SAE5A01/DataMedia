from pymongo.collection import Collection

from src.db.schemas.voyage_schemas import VoyageBase

# CRUD pour MongoDB
def create_voyage(collection: Collection, trajet: VoyageBase):
    result = collection.insert_one(trajet.dict())
    return str(result.inserted_id)

def get_voyage(collection: Collection, user_id: int):
    return collection.find_one({"idUser": user_id})