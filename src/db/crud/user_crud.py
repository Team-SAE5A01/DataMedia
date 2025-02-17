from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from passlib.context import CryptContext

from src.db.models.user_models import Client, Assistant, User
from src.db.schemas.user_schemas import UserUpdate
from src.db.schemas.auth_schema import RegisterSchema

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def create_user(db: Session, user: RegisterSchema):
    """
    Registers a new user dynamically into Clients or Assistants.
    """
    # Ensure email is unique
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    if user.mot_de_passe != user.confirm_mot_de_passe:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = hash_password(user.mot_de_passe)

    # Shared fields
    user_data = {
        "email": user.email,
        "mot_de_passe": hashed_password,
        "date_naissance": user.date_naissance,
        "nom": user.nom,
        "prenom": user.prenom,
        "role": user.role
    }

    new_user = None
    # Instantiate the correct subclass
    if user.role == "client":
        user_data["type_handicap"] = user.type_handicap
        new_user = Client(**user_data)
    elif user.role == "assistant":
        new_user = Assistant(**user_data)
    else:
        raise HTTPException(status_code=400, detail="Invalid role provided")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by email from the Users table.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_id(db: Session, id: int):
    """
    Retrieve a user by email from the Users table.
    """
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """
    Update an existing user's information.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

def delete_user(db: Session, user_id: int):
    """
    Delete a user from the database.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully!"}
