from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient


MYSQL_PORT=3306
MONGO_PORT=27017

USERNAME="root"
PASSWORD="JesusATM12"
REMOTE_HOST="172.31.36.57"
DATABASE="Wheeltrip"

# Configuration MySQL
class MySqlConf():
    def launch_engine(self):
        MYSQL_ENGINE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{REMOTE_HOST}:{MYSQL_PORT}/{DATABASE}"
        
        engine = create_engine(MYSQL_ENGINE_URL)
        
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        Base = declarative_base()

        return engine, SessionLocal, Base

# Usage
engine, SessionLocal, Base = MySqlConf().launch_engine() 

# Configuration MongoDB
class MongoConf():
    def get_connection(self):
        MONGO_DATABASE_URL = f"mongodb://{USERNAME}:{PASSWORD}@{REMOTE_HOST}:{MONGO_PORT}/"
        return MongoClient(MONGO_DATABASE_URL)[DATABASE]
    
mongo_db = MongoConf().get_connection()