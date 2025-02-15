from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# -------------------------------
# User Schemas
# -------------------------------

class UserBase(BaseModel):
    """
    Base model for user-related information.

    Attributes:
    - **nom**: Last name of the user.
    - **prenom**: First name of the user.
    - **date_de_naissance**: Date of birth of the user (YYYY-MM-DD format).
    - **email**: User's email address.
    """
    nom: str
    prenom: str
    date_de_naissance: date
    email: str


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Inherits from `UserBase` and adds:
    - **mot_de_passe**: The user's password (hashed before storing).
    """
    mot_de_passe: str


class UserUpdate(BaseModel):
    """
    Schema for updating user information.

    All fields are optional, allowing partial updates:
    - **nom**: Updated last name (if provided).
    - **prenom**: Updated first name (if provided).
    - **date_de_naissance**: Updated date of birth (if provided).
    - **email**: Updated email address (if provided).
    - **mot_de_passe**: Updated password (if provided).
    """
    nom: Optional[str] = None
    prenom: Optional[str] = None
    date_de_naissance: Optional[date] = None
    email: Optional[EmailStr] = None
    mot_de_passe: Optional[str] = None


class UserResponse(UserBase):
    """
    Schema for returning user data in API responses.

    Inherits from `UserBase` and adds:
    - **id**: Unique identifier of the user.
    - **date_creation**: Timestamp indicating when the user was created.
    """
    id: int
    date_creation: datetime

    class Config:
        orm_mode = True  # Enables compatibility with ORM models.


# -------------------------------
# Handicap Schemas
# -------------------------------

class HandicapBase(BaseModel):
    """
    Base model for handicap-related information.

    Attributes:
    - **nom**: Name of the handicap type.
    """
    nom: str


# -------------------------------
# Client Schemas
# -------------------------------

class ClientCreate(BaseModel):
    """
    Schema for creating a client.

    Attributes:
    - **id**: Unique identifier of the client.
    - **id_handicap**: Optional reference to the associated handicap.
    """
    id: int
    id_handicap: Optional[int]


# -------------------------------
# Company (Compagnie) Schemas
# -------------------------------

class CompagnieBase(BaseModel):
    """
    Base model for company-related information.

    Attributes:
    - **nom**: Name of the company.
    """
    nom: str


# -------------------------------
# Assistant Schemas
# -------------------------------

class AssistantCreate(BaseModel):
    """
    Schema for creating an assistant.

    Attributes:
    - **id**: Unique identifier of the assistant.
    - **id_compagnie**: ID of the company the assistant is associated with.
    """
    id: int
    id_compagnie: int
