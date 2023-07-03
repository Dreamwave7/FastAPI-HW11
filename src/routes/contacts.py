from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from src.database.db import get_db
from src.schemas import *
from src.repository import contacts as con
from sqlalchemy.orm import Session

router = APIRouter(prefix="/contacts")

@router.get("/", response_model=List[ContactModel])

@router.post("/create")
async def create_contact(body: ContactModel, db:Session = Depends(get_db)):
    res = await con.create_new_contact(body, db)
    return res


async def contacts(db :Session = Depends(get_db)):
    res = await con.get_contacts(db)
    return res


@router.get("/birthdays", response_model=List[ContactModel])
async def get_birthdays(db:Session = Depends(get_db)):
    res = await con.birthdays_7(db)
    return res


@router.get("/{contact_id}")
async def read_note(contact_id:int, db:Session = Depends(get_db)):
    res = await con.get_contact(contact_id, db)
    return res


@router.patch("/change")
async def change(body:ContactUpdate, db:Session = Depends(get_db)):
    res = await con.change_contact(body, db)
    return res

@router.delete("/delete")
async def delete(name:ContactName, db:Session = Depends(get_db)):
    res = await con.delete(name, db)
    return res

@router.post("/find/name")
async def search_name(username:ContactName, db:Session = Depends(get_db)):
    res = await con.find_name(username, db)
    return res


@router.post("/find/birthday", response_model= List[ContactModel])
async def search_birthday(birthday:ContactBirthday, db:Session = Depends(get_db)):
    res = await con.find_birthday(birthday, db)
    return res

@router.post("/find/lastname", response_model= List[ContactModel])
async def search_lastname(lastname:ContactLastname, db: Session = Depends(get_db)):
    res = await con.find_lastname(lastname, db)
    return res

@router.get("/birthdays")
async def get_birthdays(db:Session = Depends(get_db)):
    res = await con.birthdays_7(db)
    return res