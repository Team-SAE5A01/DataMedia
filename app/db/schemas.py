from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class UserBase(BaseModel):
    nom: str
    prenom: str
    date_de_naissance: date
    email: str

class UserCreate(UserBase):
    mot_de_passe: str

class UserResponse(UserBase):
    id: int
    date_creation: datetime

    class Config:
        orm_mode = True

class HandicapBase(BaseModel):
    nom: str

class ClientCreate(BaseModel):
    id: int
    id_handicap: Optional[int]

class CompagnieBase(BaseModel):
    nom: str

class AssistantCreate(BaseModel):
    id: int
    id_compagnie: int

# Schémas pour MongoDB
class Step(BaseModel):
    idTrajet: int
    idAssistant: int
    idTransport: int
    dateHeureDepart: datetime
    dateHeureArrive: datetime
    bagageDepart: int
    bagageArrive: int

class TrajetBase(BaseModel):
    idUser: int
    lieuDepart: str
    lieuArrivé: str
    dateCréation: datetime
    etat: str
    steps: List[Step]

class Transport(BaseModel):
    _id: int
    nom: str
