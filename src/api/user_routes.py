from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.schemas.user_schemas import UserResponse, UserCreate, UserUpdate
from src.db.models import user_models
from src.core import config
from src.db.crud import user_crud

router = APIRouter(tags=["Users"])

def get_db():
    """
    Dependency function to provide a database session.
    """
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get a user by ID
@router.get("/users/id/{user_id}", response_model=UserResponse, summary="Retrieve a user by ID", description="Fetches user details using the user's unique ID.")
def get_user_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by their ID.

    - **user_id**: The unique identifier of the user
    - **Returns**: User details if found, otherwise raises a 404 error.
    """
    db_user = user_crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Get a user by email
@router.get("/users/email/{user_mail}", response_model=UserResponse, summary="Retrieve a user by email", description="Fetches user details using their registered email address.")
def get_user_email(user_mail: str, db: Session = Depends(get_db)):
    """
    Get a user by their email address.

    - **user_mail**: The email address of the user
    - **Returns**: User details if found, otherwise raises a 404 error.
    """
    db_user = user_crud.get_user_by_email(db, user_mail)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update a user
@router.put("/users/{user_id}", response_model=UserResponse, summary="Update user details", description="Updates the details of an existing user using their unique ID.")
def update_user_route(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update user information.

    - **user_id**: The unique identifier of the user
    - **user_update**: JSON payload containing updated user details
    - **Returns**: The updated user details
    """
    updated_user = user_crud.update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Delete a user
@router.delete("/users/{user_id}", summary="Delete a user", description="Deletes a user from the system using their unique ID.")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user.

    - **user_id**: The unique identifier of the user to be deleted
    - **Returns**: A success message if the user was deleted, otherwise raises a 404 error.
    """
    deleted_user = user_crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# List all users
@router.get("/users/", response_model=list[UserResponse], summary="List all users", description="Retrieves a list of all registered users.")
def list_users_route(db: Session = Depends(get_db)):
    """
    Retrieve a list of all users.

    - **Returns**: A list of user details
    """
    return db.query(user_models.User).all()
