from sqlalchemy import Enum  # Correct
from sqlalchemy import Boolean, Column, Integer, String, Date, TIMESTAMP, ForeignKey
from src.core.config import Base

# -------------------------------
# User Model (Base for Clients & Assistants)
# -------------------------------

class User(Base):
    """
    Represents a user with shared fields for Clients and Assistants.
    """
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(Enum("client", "assistant", name="role_enum"), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    mot_de_passe = Column(String(255), nullable=False)
    date_naissance = Column(Date, nullable=True)
    nom = Column(String(100), nullable=True)
    prenom = Column(String(100), nullable=True)
    date_creation = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": role
    }

# -------------------------------
# Client Model (Inherits from User)
# -------------------------------

class Client(User):
    """
    Represents a client, inheriting from User.
    """
    __tablename__ = "Client"

    id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    type_handicap = Column(Enum("visuel", "auditif", "cognitif", "moteur", name="handicap_enum"), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "client",
    }

# -------------------------------
# Assistant Model (Inherits from User)
# -------------------------------

class Assistant(User):
    """
    Represents an assistant, inheriting from User.
    """
    __tablename__ = "Assistant"

    id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    disponible = Column(Boolean, default=True)  # Availability status

    __mapper_args__ = {
        "polymorphic_identity": "assistant",
    }
