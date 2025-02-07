from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path

ENVIRONMENT = os.getenv('ENVIRONMENT', "local")

if ENVIRONMENT == 'local':
    aws_backend_hostname = os.getenv("LOCALHOST")
    aws_frontend_hostname = os.getenv("LOCALHOST")
elif ENVIRONMENT == 'production':
    aws_backend_hostname = os.getenv("AWS_BACKEND_IP")
    aws_frontend_hostname = os.getenv("AWS_FRONTEND_IP")

else:
    aws_backend_hostname = os.getenv("LOCALHOST") 
    aws_frontend_hostname = os.getenv("LOCALHOST")

BACKEND_HOSTNAME=aws_backend_hostname
FRONTEND_HOSTNAME=aws_frontend_hostname

MYSQL_PORT=os.getenv("MYSQL_PORT")
MONGO_PORT=os.getenv("MONGODB_PORT")
WHEELTRIP_USER_PORT=os.getenv("WHEELTRIP_USER_PORT")

USERNAME=os.getenv("DATABASE_USERNAME")
PASSWORD=os.getenv("DATABASE_PASSWORD")
DATABASE=os.getenv("DATABASE_NAME")
REQUEST_PROTOCOL=os.getenv("REQUEST_PROTOCOL")

# Configuration MySQL
class MySqlConf():
    def launch_engine(self):
        MYSQL_ENGINE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{BACKEND_HOSTNAME}:{MYSQL_PORT}/{DATABASE}"
        
        engine = create_engine(MYSQL_ENGINE_URL)
        
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        Base = declarative_base()

        return engine, SessionLocal, Base

# Usage
engine, SessionLocal, Base = MySqlConf().launch_engine() 

# Configuration MongoDB
class MongoConf():
    def get_connection(self):
        MONGO_DATABASE_URL = f"mongodb://{USERNAME}:{PASSWORD}@{BACKEND_HOSTNAME}:{MONGO_PORT}/"
        return MongoClient(MONGO_DATABASE_URL)[DATABASE]
    
mongo_db = MongoConf().get_connection()