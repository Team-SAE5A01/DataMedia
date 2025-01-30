from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

username = "root"
password = "JesusATM12"
host = "54.174.50.209:3306"  # Change if using a remote server
database_name = "Wheeltrip"

# Configuration MySQL
engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}")
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Configuration MongoDB
MONGO_DATABASE_URL = "mongodb://root:JesusATM12@54.174.50.209:27017/"
mongo_client = MongoClient(MONGO_DATABASE_URL)
mongo_db = mongo_client["my_mongo_db"]  # Remplace par le nom de ta DB
