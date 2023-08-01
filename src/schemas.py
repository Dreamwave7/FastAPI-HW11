from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from src.database.models import *


class UserDB(BaseModel):
    id:str
    username:str
    email:str
    password:str
    refresh_token: None

    class Config:
        orm_mode = True    

class UserModel(BaseModel):
    email: str
    username:str
    password: str


class UserResponse(BaseModel):
    user:UserDB
    detail:str

class TokenModel(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str

class ContactModel(BaseModel):
    name : str
    lastname: str
    email:str
    phone: str
    birthday: str
    user_id :int

    class Config:
        orm_mode = True

class ContactUpdate(BaseModel):
    name:str
    lastname:str
    email:str
    phone:str
    birthday:str



class ContactName(BaseModel):
    name:str



class ContactBirthday(BaseModel):
    birthday:str



class ContactLastname(BaseModel):
    lastname:str

 