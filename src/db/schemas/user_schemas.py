from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class UserBase(BaseModel):
    nom: str
    prenom: str
    date_de_naissance: date
    email: str

class UserCreate(UserBase):
    mot_de_passe: str

class UserUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    date_de_naissance: Optional[date] = None
    email: Optional[EmailStr] = None
    mot_de_passe: Optional[str] = None

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