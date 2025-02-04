from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path

environment = os.getenv('ENVIRONMENT', 'local')

if environment == 'local':
    hostname = os.getenv("LOCALHOST")
elif environment == 'production':
    hostname = os.getenv("AWS_BACKEND_IP") 
else:
    hostname = os.getenv("LOCALHOST") 

MYSQL_PORT=os.getenv("AWS_MYSQL_PORT")
MONGO_PORT=os.getenv("AWS_MONGODB_PORT")

HOSTNAME=hostname
USERNAME=os.getenv("AWS_DATABASE_USERNAME")
PASSWORD=os.getenv("AWS_DATABASE_PASSWORD")
DATABASE=os.getenv("AWS_DATABASE_NAME")

# Configuration MySQL
class MySqlConf():
    def launch_engine(self):
        MYSQL_ENGINE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOSTNAME}:{MYSQL_PORT}/{DATABASE}"
        
        engine = create_engine(MYSQL_ENGINE_URL)
        
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        Base = declarative_base()

        return engine, SessionLocal, Base

# Usage
engine, SessionLocal, Base = MySqlConf().launch_engine() 

# Configuration MongoDB
class MongoConf():
    def get_connection(self):
        MONGO_DATABASE_URL = f"mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}:{MONGO_PORT}/"
        return MongoClient(MONGO_DATABASE_URL)[DATABASE]
    
mongo_db = MongoConf().get_connection()