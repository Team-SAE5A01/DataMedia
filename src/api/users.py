from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.schemas.user_schemas import UserResponse, UserCreate, UserUpdate
from src.db.models import user_models
from src.core import config
from src.db.crud import user_crud

router = APIRouter()

def get_db():
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a user
@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db, user)

# Get a user by ID
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Get a user by email
@router.get("/users/{user_mail}", response_model=UserResponse)
def get_user_email(user_mail: str, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, user_mail)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update a user
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    updated_user = user_crud.update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Delete a user
@router.delete("/users/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    deleted_user = user_crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# List all users
@router.get("/users/", response_model=list[UserResponse])
def list_users_route(db: Session = Depends(get_db)):
    return db.query(user_models.User).all()