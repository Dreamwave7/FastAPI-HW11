from typing import List

from sqlalchemy.orm import Session

from src.database.models import *
from src.schemas import *
from datetime import datetime, timedelta


async def get_contacts(db:Session):
    q = db.query(Contacts).all()
    return q

async def get_contact(contact_id:int, db:Session):
    res = db.query(Contacts).filter(Contacts.id == contact_id).first()
    return res

async def create_new_contact(body:ContactModel, db: Session):
    user = Contacts(name = body.name, lastname = body.lastname, email = body.email, phone = body.phone, birthday = body.birthday)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

async def change_contact(body:ContactUpdate, db:Session):
    res = db.query(Contacts).filter(Contacts.name == body.name).first()
    res.birthday = body.birthday
    res.email = body.email
    res.phone = body.phone
    db.commit()
    db.refresh(res)
    return  res

async def delete(name:ContactName, db:Session):
    res = db.query(Contacts).filter(Contacts.name == name.name).first()
    db.delete(res)
    db.commit()
    return res

async def find_name(username:ContactName, db:Session):
    res = db.query(Contacts).filter(Contacts.name == username.name).first()
    return res

async def find_birthday(birthday:ContactBirthday, db :Session):
    res = db.query(Contacts).filter(Contacts.birthday == birthday.birthday).all()
    return res

async def find_lastname(lastname:ContactLastname, db:Session):
    res = db.query(Contacts).filter(Contacts.lastname == lastname.lastname).all()
    return res

async def birthdays_7(db:Session):
    users = db.query(Contacts).all()
    birthdays_list = []

    for user in users:
        birth = verify_date(user.birthday)
        if birth:
            birthdays_list.append(user)
        else:
            continue
    return birthdays_list



def verify_date(date:str):
    current = datetime.now().date()
    year = current.year
    current_7 = current + timedelta(days=7)
    user_date = datetime.strptime(date, "%d.%m.%Y").date().replace(year=year)

    if current < user_date < current_7:
        return True
    else:
        return False