from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer  # Import authentication scheme
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.core.config import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from src.db.crud.user_crud import get_user_by_email, create_user
from src.core import config
from src.db.schemas.auth_schema import LoginSchema, RegisterSchema

# Define API router
router = APIRouter()

# OAuth2 authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    """
    Dependency function to get a database session.
    Ensures that the session is closed after use.
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
    Verify if a plain text password matches the stored hashed password.
    
    Args:
        plain_password (str): User-provided password.
        hashed_password (str): Hashed password stored in the database.
    
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(email: str, password: str, db: Session):
    """
    Authenticate a user by validating their email and password.
    
    Args:
        email (str): User's email.
        password (str): User's password.
        db (Session): Database session.
    
    Returns:
        User object if authentication is successful, False otherwise.
    """
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.mot_de_passe):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a JSON Web Token (JWT) for authenticated users.
    
    Args:
        data (dict): Data to encode in the token.
        expires_delta (Optional[timedelta]): Token expiration time.
    
    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", 
    status_code=status.HTTP_201_CREATED,
    response_model=dict, 
    tags=["Authentication"],
    description="Register a new user with provided details in the database and return an access token :\n\n"
                "Roles :\n"
                "- **1**: Client\n"
                "- **2**: Assistant\n"
                "- **3**: Manager\n"
                "- **4**: Admin"
)
async def register_user(user: RegisterSchema, db: Session = Depends(get_db)):
    """
    Register a new user and return an access token.
    
    Args:
        user (RegisterSchema): User registration data.
        db (Session): Database session.
    
    Returns:
        dict: Access token and token type.
    """
    new_user = create_user(user, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"id": new_user.id, "sub": new_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=dict, tags=["Authentication"])
async def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    """
    Authenticate user and generate a JWT access token.
    
    Args:
        login_data (LoginSchema): Login credentials.
        db (Session): Database session.
    
    Returns:
        dict: Access token and token type.
    
    Raises:
        HTTPException: If authentication fails.
    """
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

@router.get("/check_token", response_model=dict, tags=["Authentication"])
async def check_token_validity(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Validate a JWT token and retrieve the associated user's details.
    
    Args:
        token (str): JWT token from request.
        db (Session): Database session.
    
    Returns:
        dict: User details (email and ID).
    
    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
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

    return {"email": user.email, "id": user.id}
