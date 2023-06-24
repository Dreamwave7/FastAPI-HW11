from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sql_key = "postgresql+psycopg2://dkwvkeys:aD0Tydu8H8DSKRQKPMEIAVSLcKK-a6CM@tyke.db.elephantsql.com/dkwvkeys"
engine = create_engine(sql_key)
session = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(200))
    done = Column(Boolean(),default=False)


Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()



