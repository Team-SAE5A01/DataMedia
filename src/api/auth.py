from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer  # Import this
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.core.config import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from src.db.crud.user_crud import get_user_by_email, register_user
from src.core import config
from src.db.schemas.auth_schema import LoginSchema, RegisterSchema

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # Define OAuth2 scheme

def get_db():
    """
    Dependency to get the database session.
    """
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(email: str, password: str, db: Session):
    """
    Authenticate user credentials by checking the email and password.
    """
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.mot_de_passe):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dict, tags=["Authentication"])
async def register(user: RegisterSchema, db: Session = Depends(get_db)):
    """
    Register a new user and return an access token.
    """
    new_user = register_user(user, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": new_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=dict, tags=["Authentication"])
async def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    """
    Authenticate user and generate a JWT token.
    """
    user = authenticate_user(login_data.email, login_data.mot_de_passe, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/check_token", response_model=dict, tags=["Authentication"])
async def check_token_validity(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Check if the provided JWT token is valid and return the associated user.

    **Returns:**
    - `200 OK`: User details if the token is valid.
    - `401 Unauthorized`: If the token is invalid, expired, or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception  # No email in token -> Invalid token

    except JWTError:
        raise credentials_exception  # Token decoding failed

    # Find the user in the database
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception  # User not found -> Invalid token

    # Return user details
    return {"email": user.email, "id": user.id}