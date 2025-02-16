from pydantic import BaseModel, EmailStr
from datetime import date

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