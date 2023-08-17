from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail,MessageType
from pydantic import EmailStr, BaseModel
from typing import List

from src.routes import contacts
from pathlib import Path

app = FastAPI()


app.include_router(contacts.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message":"Hello dima"}



































































