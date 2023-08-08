from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_
from src.database.models import *
from src.schemas import *
from datetime import datetime, timedelta


async def get_contacts(user:User,db:Session) -> List[Contacts]:
    result = db.query(Contacts).filter(Contacts.user_id == user.id).all()
    return result

async def get_contact(contact_id:int, user:User, db:Session):
    res = db.query(Contacts).filter(and_(Contacts.id == contact_id,Contacts.user_id == user.id)).first()
    return res



async def create_new_contact(body:ContactModel,user :User, db: Session):
    new_contact = Contacts(name = body.name,
                    lastname = body.lastname,
                    email = body.email,
                    phone = body.phone,
                    birthday = body.birthday,
                    user_id = user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

async def birthdays_7(user:User , db:Session):
    users = db.query(Contacts).filter(Contacts.user_id == user.id).all()
    birthdays_list = []

    for user in users:
        birth = verify_date(user.birthday)
        if birth:
            birthdays_list.append(user)
        else:
            continue
    return birthdays_list


async def delete_contact(contact_id, user:User, db:Session):
    res = db.query(Contacts).filter(and_(Contacts.user_id == user.id, Contacts.id == contact_id)).first()
    db.delete(res)
    db.commit()
    return res


async def find_name(username:ContactName,user:User, db:Session):
    result = db.query(Contacts).filter(and_(Contacts.user_id == user.id, Contacts.name == username.name)).first()
    return result

async def find_birthday(birthday:ContactBirthday,user:User, db :Session):
    res = db.query(Contacts).filter(and_(Contacts.user_id == user.id, Contacts.birthday == birthday.birthday)).first()
    return res

async def change_contact(contact_id:int, body:ContactUpdate,user:User, db:Session):
    user = db.query(Contacts).filter(and_(Contacts.user_id == user.id, Contacts.id == contact_id)).first()
    user.birthday = body.birthday
    user.email = body.email
    user.phone = body.phone
    db.commit()
    db.refresh(user)
    return  user


async def find_lastname(lastname:ContactLastname,user:User, db:Session):
    res = db.query(Contacts).filter(and_(Contacts.user_id == user.id, Contacts.lastname == lastname.lastname)).first()
    return res




def verify_date(date:str):
    current = datetime.now().date()
    year = current.year
    current_7 = current + timedelta(days=7)
    user_date = datetime.strptime(date, "%d.%m.%Y").date().replace(year=year)

    if current < user_date < current_7:
        return True
    else:
        return False
    
