from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class UserModel(BaseModel):
    email: str
    password: str
    refresh_token: str



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

 