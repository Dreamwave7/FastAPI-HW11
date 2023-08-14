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
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), default=None)
    user = relationship("User", backref="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100),nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(300), nullable= False, unique=True)
    refresh_token = Column(String(300), nullable=True)
    confirmed = Column(Boolean,default=False)

    






























