from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from .config import Base

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    date_de_naissance = Column(Date, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    mot_de_passe = Column(String(255), nullable=False)
    date_creation = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

class Handicap(Base):
    __tablename__ = "Handicap"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100), nullable=False)

class Client(Base):
    __tablename__ = "Client"

    id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    id_handicap = Column(Integer, ForeignKey("Handicap.id"), nullable=True)

class Compagnie(Base):
    __tablename__ = "Compagnie"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)

class Assistant(Base):
    __tablename__ = "Assistant"

    id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    id_compagnie = Column(Integer, ForeignKey("Compagnie.id"), nullable=False)
