from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import schemas
from app.core import config
from app.db.crud import users

router = APIRouter()

def get_db():
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/test")
def def_test():
    return {
        "Test" : "Hello great people!",
        "ENV" : config.ENVIRONMENT,
        "BACKEND_HOST" : config.BACKEND_HOSTNAME,
        "FRONT_HOST" : config.FRONTEND_HOSTNAME,
        "MYSQL_PORT" : config.MYSQL_PORT,
        "MONGO_PORT" : config.MONGO_PORT,
        "WHEELTRIP_USER_PORT" : config.WHEELTRIP_USER_PORT,
        "USERNAME" : config.USERNAME,
        "PASSWORD" : config.PASSWORD,
        "DATABASE" : config.DATABASE,
        "REQUEST_PROTOCOL" : config.REQUEST_PROTOCOL,
        }