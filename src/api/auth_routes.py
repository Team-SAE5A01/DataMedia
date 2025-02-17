from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.core.config import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from src.db.crud.user_crud import get_user_by_email, create_user
from src.db.schemas.auth_schema import LoginSchema, RegisterSchema

# Define API router
router = APIRouter()

# OAuth2 authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    """
    Dependency function to get a database session.
    Ensures that the session is closed after use.
    """
    from src.core.config import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    """
    Hashes the password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a plain text password matches the stored hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(email: str, password: str, db: Session):
    """
    Authenticate a user by validating their email and password.
    Returns the user object if authentication is successful, otherwise returns False.
    """
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.mot_de_passe):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a JWT for authenticated users.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", 
    status_code=status.HTTP_201_CREATED,
    response_model=dict, 
    tags=["Authentication"],
    summary="Register a new user",
    description="""
    Creates a new user account. The user must provide an email, password, and role.
    Passwords must match for registration to be successful.
    Returns an access token upon successful registration.
    """
)
async def register_user(user_data: RegisterSchema, db: Session = Depends(get_db)):
    if user_data.mot_de_passe != user_data.confirm_mot_de_passe:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    new_user = create_user(db, user_data)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"id": new_user.id, "sub": new_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", 
    response_model=dict, 
    tags=["Authentication"],
    summary="User login",
    description="""
    Authenticates a user using their email and password.
    Returns an access token if credentials are valid.
    """
)
async def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(login_data.email, login_data.mot_de_passe, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"id": user.id, "sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/check_token", 
    response_model=dict, 
    tags=["Authentication"],
    summary="Validate access token",
    description="""
    Validates the provided JWT access token and returns the associated user information.
    If the token is invalid or expired, an error response is returned.
    """
)
async def check_token_validity(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return {"email": user.email, "id": user.id, "role": user.role}
