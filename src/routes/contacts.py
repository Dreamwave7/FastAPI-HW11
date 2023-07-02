from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from src.database.db import get_db
from src.schemas import *
from src.repository import contacts as con
from sqlalchemy.orm import Session

router = APIRouter(prefix="/contacts")

@router.get("/", response_model=List[ContactModel])
async def contacts(db :Session = Depends(get_db)):
    res = await con.get_contacts(db)
    return res
    

@router.get("/{contact_id}")
async def read_note(contact_id:int, db:Session = Depends(get_db)):
    res = await con.get_contact(contact_id, db)
    return res

@router.post("/create/")
async def create_contact(body: ContactModel, db:Session = Depends(get_db)):
    res = await con.create_new_contact(body, db)
    return res


# @router.post("/",response_model=NoteResponse)
# async def create_note(body:NoteModel, db:Session= Depends(get_db)):
#     return await rep_notes.create_note(body,db)

# @router.put("/{note_id}",response_model=NoteResponse)
# async def update_note(body: NoteUpdate, note_id:int, db:Session = Depends(get_db)):
#     note = await rep_notes.update_note(note_id, body, db)
#     if note is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
#     return note

# @router.patch("/{note_id}", response_model=NoteResponse)
# async def update_status_code(body: NoteStatusUpdate, note_id:int, db: Session = Depends(get_db)):
#     note = await rep_notes.update_status(note_id, body, db)
#     if note is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    

# @router.delete("/{note_id}", response_model=NoteResponse)
# async def remove_note(note_id: int, db:Session = Depends(get_db)):
#     note = await rep_notes.remove_note(note_id, db)
#     return note