from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
from dopplersdk import DopplerSDK
import os

# Doppler config
access_token = "dp.st.prd.QamSTwT1Gd3mgJosbdWPrtoS6LgF4L98PxFjZ8TwNeA"
doppler_config = "prd"
doppler_project = "wheeltrip"

# Initialize Doppler secrets management
doppler = DopplerSDK()
doppler.set_access_token(access_token)

def get_secret(name, config=doppler_config, project=doppler_project):
    return doppler.secrets.get(name, config, project).value['raw']

ENVIRONMENT = os.getenv("NEXT_PUBLIC_BUILD_ENV", "UNDEFINED")

if ENVIRONMENT == 'local':
    backend_hostname = get_secret("NEXT_PUBLIC_LOCALHOST")
    frontend_hostname = get_secret("NEXT_PUBLIC_LOCALHOST")
elif ENVIRONMENT == 'production':
    backend_hostname = get_secret("NEXT_PUBLIC_AWS_BACKEND_IP")
    frontend_hostname = get_secret("NEXT_PUBLIC_AWS_FRONTEND_IP")
else:
    backend_hostname = get_secret("NEXT_PUBLIC_LOCALHOST")
    frontend_hostname = get_secret("NEXT_PUBLIC_LOCALHOST")

BACKEND_HOSTNAME = backend_hostname
FRONTEND_HOSTNAME = frontend_hostname

MYSQL_PORT = get_secret("NEXT_PUBLIC_MYSQL_PORT")
MONGO_PORT = get_secret("NEXT_PUBLIC_MONGODB_PORT")
WHEELTRIP_USER_PORT = get_secret("NEXT_PUBLIC_WHEELTRIP_USER_PORT")

USERNAME = get_secret("NEXT_PUBLIC_DATABASE_USERNAME")
PASSWORD = get_secret("NEXT_PUBLIC_DATABASE_PASSWORD")
DATABASE = get_secret("NEXT_PUBLIC_DATABASE_NAME")
REQUEST_PROTOCOL = get_secret("NEXT_PUBLIC_REQUEST_PROTOCOL")

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