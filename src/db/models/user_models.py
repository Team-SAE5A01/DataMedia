from enum import Enum
from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP
from sqlalchemy import Enum as SQLAlchemyEnum
from src.core.config import Base

# -------------------------------
# User Model
# -------------------------------

class RoleEnum(int, Enum):
    CLIENT = 1
    ASSISTANT = 2
    MANAGER = 3
    ADMIN = 4

class User(Base):
    """
    Represents a user in the system.

    Attributes:
    - **id (int)**: Auto-incrementing primary key.
    - **nom (str)**: Last name of the user (max 100 characters).
    - **prenom (str)**: First name of the user (max 100 characters).
    - **date_de_naissance (date)**: User's date of birth.
    - **email (str)**: Unique email address (max 255 characters).
    - **mot_de_passe (str)**: Hashed password (max 255 characters).
    - **date_creation (timestamp)**: Timestamp of user creation (default: current timestamp).
    """
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100), nullable=True)
    prenom = Column(String(100), nullable=True)
    date_de_naissance = Column(Date, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    date_creation = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

# -------------------------------
# Client Model
# -------------------------------

class Client(Base):
    """
    Represents a client who is a user and may have a specific handicap.

    Attributes:
    - **id (int)**: Foreign key referencing `User.id`, acts as the primary key.
    - **id_handicap (int, optional)**: Foreign key referencing `Handicap.id` (nullable).
    """
    __tablename__ = "Client"

    id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    id_handicap = Column(Integer, ForeignKey("Handicap.id"), nullable=True)

# -------------------------------
# Handicap Model
# -------------------------------

class HandicapEnum(Enum):
    MOTEUR = 1
    VISUEL = 2
    AUDITIF = 3
    COGNITIF = 4


class Handicap(Base):
    """
    Represents different types of handicaps.

    Attributes:
    - **id (int)**: Auto-incrementing primary key.
    - **nom (str)**: Name of the handicap type (max 100 characters).
    """
    __tablename__ = "Handicap"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100), nullable=False)

# -------------------------------
# Compagnie Model
# -------------------------------

class Compagnie(Base):
    """
    Represents a company that employs assistants.

    Attributes:
    - **id (int)**: Auto-incrementing primary key.
    - **nom (str)**: Name of the company (max 100 characters).
    """
    __tablename__ = "Compagnie"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)


# -------------------------------
# Assistant Model
# -------------------------------

class Assistant(Base):
    """
    Represents an assistant who is a user and assits a client.

    Attributes:
    - **id (int)**: Foreign key referencing `User.id`, acts as the primary key.
    """
    __tablename__ = "Assistant"

    id = Column(Integer, ForeignKey("User.id"), primary_key=True)

# -------------------------------
# Manager Model
# -------------------------------

class Manager(Base):
    """
    Represents a manager who is a user and works for a company.

    Attributes:
    - **id (int)**: Foreign key referencing `User.id`, acts as the primary key.
    - **id_compagnie (int)**: Foreign key referencing `Compagnie.id` (not nullable).
    """
    __tablename__ = "Manager"

    id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    id_compagnie = Column(Integer, ForeignKey("Compagnie.id"), nullable=False)

# -------------------------------
# User roles Model
# -------------------------------

class user_roles(Base):
    """
    Represents the different user roles that can be affected to an user.

    Attributes:
    - **id (int)**: Auto-incrementing primary key.
    - **role (str)**: Name of the role (max 100 characters).
    """
    __tablename__ = 'user_roles'  # Adjust table name if needed

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(100), nullable=False)