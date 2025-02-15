from pydantic import BaseModel
from typing import List
from datetime import datetime

# Schémas pour MongoDB
class Step(BaseModel):
    idTrajet: int
    idAssistant: int
    idTransport: int
    dateHeureDepart: datetime
    dateHeureArrive: datetime
    bagageDepart: int
    bagageArrive: int

class VoyageBase(BaseModel):
    idUser: int
    lieuDepart: str
    lieuArrivé: str
    dateCréation: datetime
    etat: str
    steps: List[Step]

class Transport(BaseModel):
    _id: int
    nom: str