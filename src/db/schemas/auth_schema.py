from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
from datetime import date
from enum import Enum

class UserRole(str, Enum):
    client = "client"
    assistant = "assistant"

class HandicapType(str, Enum):
    visuel = "visuel"
    auditif = "auditif"
    cognitif = "cognitif"
    moteur = "moteur"

class LoginSchema(BaseModel):
    """
    Schema for user login.
    """
    email: EmailStr
    mot_de_passe: str

class RegisterSchema(BaseModel):
    """
    Schema for user registration. Handles Clients, Assistants, and other roles.
    """
    email: EmailStr
    mot_de_passe: str
    confirm_mot_de_passe: str
    role: UserRole
    date_naissance: Optional[date] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None

    # Client-specific fields
    type_handicap: Optional[HandicapType] = None

    # Assistant-specific fields
    disponible: Optional[bool] = None

    class Config:
        use_enum_values = True  # Ensures enum values are stored as strings

    @model_validator(mode="before")
    def validate_role_fields(cls, values):
        """
        Ensures only relevant fields are provided based on the user's role.
        """
        role = values.get("role")
        type_handicap = values.get("type_handicap")
        disponible = values.get("disponible")

        # Clients must have a handicap
        if role == "client":
            if type_handicap is None:
                raise ValueError("Clients must have a handicap type.")
            if disponible is not None:
                raise ValueError("Clients should not have a 'disponible' field.")

        # Assistants cannot have a handicap but can have 'disponible'
        elif role == "assistant":
            if type_handicap is not None:
                raise ValueError("Assistants cannot have a handicap type.")
            if disponible is None:
                values["disponible"] = True  # Default to True if not provided

        return values

    @model_validator(mode="before")
    def check_passwords_match(cls, values):
        """
        Ensures password and confirmation match.
        """
        if values.get("mot_de_passe") != values.get("confirm_mot_de_passe"):
            raise ValueError("Passwords do not match.")
        return values