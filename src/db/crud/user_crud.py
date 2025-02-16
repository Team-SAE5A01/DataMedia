from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from passlib.context import CryptContext

from src.db.models.user_models import User
from src.db.schemas.user_schemas import UserCreate, UserUpdate
from src.db.schemas.auth_schema import RegisterSchema

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): SQLAlchemy database session.
        user (UserCreate): User creation schema containing:
            - nom (str): Last name of the user.
            - prenom (str): First name of the user.
            - date_de_naissance (date): User's birth date.
            - email (str): Unique email address.
            - mot_de_passe (str): Hashed password.

    Returns:
        User: The newly created user object.

    Raises:
        HTTPException (400): If the email already exists in the database.
    """
    try:
        hash_mot_de_passe = hash_password(user.mot_de_passe)
        db_user = User(
            nom=user.nom,
            prenom=user.prenom,
            date_de_naissance=user.date_de_naissance,
            email=user.email,
            mot_de_passe=hash_mot_de_passe,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    
def register_user(user: RegisterSchema, db: Session):
    """
    Register a new user in the database with only date of birth, email, and password.

    Args:
        db (Session): SQLAlchemy database session.
        user (UserCreate): User creation schema containing:
            - date_de_naissance (date): User's birth date.
            - email (str): Unique email address.
            - mot_de_passe (str): Hashed password.

    Returns:
        User: The newly created user object.

    Raises:
        HTTPException (400): If the email already exists in the database.
    """
    if user.mot_de_passe != user.confirm_mot_de_passe:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    hash_mot_de_passe = hash_password(user.mot_de_passe)

    try:
        db_user = User(
            date_de_naissance=user.date_de_naissance,
            email=user.email,
            mot_de_passe=hash_mot_de_passe,
        )
        print(db_user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

def get_user(db: Session, user_id: int):
    """
    Retrieve a user by their unique ID.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): The ID of the user.

    Returns:
        User: The user object if found.

    Raises:
        HTTPException (404): If the user is not found.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by their email address.

    Args:
        db (Session): SQLAlchemy database session.
        email (str): The email of the user.

    Returns:
        User: The user object if found.

    Raises:
        HTTPException (404): If the user is not found.
    """
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """
    Update an existing user's information.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): The ID of the user to update.
        user_update (UserUpdate): Fields to update (partial update allowed).

    Returns:
        User: The updated user object.

    Raises:
        HTTPException (404): If the user is not found.
        HTTPException (400): If updating the email to an existing one causes a conflict.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")


def delete_user(db: Session, user_id: int):
    """
    Delete a user from the database.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): The ID of the user to delete.

    Returns:
        User: The deleted user object.

    Raises:
        HTTPException (404): If the user is not found.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
