from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.conf.config import settings

sql_key = settings.sql_key
engine = create_engine(sql_key)
session = sessionmaker(autocommit = False, autoflush=False, bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()



