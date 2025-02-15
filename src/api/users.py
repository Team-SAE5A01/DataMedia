from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.schemas.user_schemas import UserResponse, UserCreate
from src.core import config
from src.db.crud import user_crud

router = APIRouter()

def get_db():
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes pour MySQL (Utilisateurs)
@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db, user)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user