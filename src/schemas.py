from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# class TagModel(BaseModel):
#     name :str = Field(max_length=25)

# class TagResponse(TagModel):
#     id :int

#     class Config:
#         orm_mode = True

# class NoteBase(BaseModel):
#     title: str = Field(max_length=200)
#     description :str = Field(max_length=200)

# class NoteModel(NoteBase):
#     tags: List[int]

# class NoteUpdate(NoteModel):
#     done :bool

# class NoteStatusUpdate(BaseModel):
#     done:bool

# class NoteResponse(NoteBase):
#     id:int
#     created_at : datetime
#     tags: List[TagResponse]

#     class Config:
#         orm_mode = True


class ContactModel(BaseModel):
    name : str
    lastname: str
    email:str
    phone: str
    birthday: str

    class Config:
        orm_mode = True

class ContactUpdate(BaseModel):
    name:str
    email:str
    phone:str
    birthday:str



class ContactName(BaseModel):
    name:str



class ContactBirthday(BaseModel):
    birthday:str



class ContactLastname(BaseModel):
    lastname:str

 