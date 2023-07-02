from typing import List

from sqlalchemy.orm import Session

from src.database.models import *
from src.schemas import *


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

# async def get_notes(skip:int, limit:int, db:Session):
#     return db.query(Note).offset(skip).limit(limit).all()

# async def get_note(note_id:int, db:Session):
#     return db.query(Note).filter(Note.id == note_id).first()

# async def create_note(body:NoteModel, db:Session):
#     tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
#     note = Note(title = body.title, description = body.description, tags = tags)
#     db.add(note)
#     db.commit()
#     db.refresh(note)
#     return note

# async def remove_note(note_id:int, db:Session):
#     note = db.query(Note).filter(Note.id == note_id).first()
#     if note:
#         db.delete(note)
#         db.commit()
#     return note

# async def update_note(note_id:int,body:NoteUpdate, db:Session):
#     note = db.query(Note).filter(Note.id == note_id).first()
#     note.title = body.title
#     note.description = body.description
#     note.done = body.done
#     note.tags = body.tags
#     db.commit()

#     return note

# async def update_status(note_id:int, body:NoteStatusUpdate, db:Session):
#     note = db.query(Note).filter(Note.id == note_id).first()
#     if note:
#         note.done = body.done
#         db.commit()
#         return note
