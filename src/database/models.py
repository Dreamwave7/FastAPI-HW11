from sqlalchemy import Column, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Contacts(Base):
    __tablename__ = "contacts"
    id = Column(Integer,primary_key=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable= False)
    email = Column(String(300),nullable=False)
    phone = Column(String(30), nullable=False)
    birthday = Column(String(25), nullable=False)