from fastapi import FastAPI, Path, Query,Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from db import get_db, Note
# uvicorn test:app --host localhost --port 8000 --reload

app = FastAPI()

class NoteModel(BaseModel):
    name: str
    description: str
    done: bool

class ResponseModel(BaseModel):
    id: int = Field(default=1, ge=1)
    name:str
    description : str
    done: bool

@app.post("/test")
def root(note :NoteModel, db :Session = Depends(get_db)):
    new_note = NoteModel(name=note.name, description=note.description, done=note.done)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@app.get("/notes")
def read_notes(skip:int = 0, limit : int = Query(default=10, le=100, ge=10), db:Session = Depends(get_db)) -> list[ResponseModel]:
    notes = db.query(Note).offset(skip).limit(limit).all()

    return notes


@app.get("/notes/{note_id}")
def read_note(note_id:int = Path(gt=0, le=10), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail= "Not found")
    return note