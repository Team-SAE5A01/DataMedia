from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from src.db.models.user_models import RoleEnum

class LoginSchema(BaseModel):
    """
    Schema for user login.
    """
    email: EmailStr
    mot_de_passe: str

class RegisterSchema(BaseModel):
    """
    Schema for user registration.
    """
    email: EmailStr
    date_de_naissance: date
    mot_de_passe: str
    confirm_mot_de_passe: str
    role: int

    @field_validator("role")
    def validate_role(cls, v):
        if v not in {role.value for role in RoleEnum}:
            raise ValueError("Invalid role value")
        return v