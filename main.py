from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail,MessageType
from pydantic import EmailStr,BaseModel
from typing import List

from src.routes import contacts
from pathlib import Path

app = FastAPI()


app.include_router(contacts.router, prefix="/api")



class EmailSchema(BaseModel):
    email:EmailStr

config = ConnectionConfig(MAIL_USERNAME="dima63475@meta.ua",
                          MAIL_PASSWORD="Zazazadima19017901",
                          MAIL_FROM="dima63475@meta.ua",
                          MAIL_PORT=465,
                          MAIL_SERVER="smtp.meta.ua",
                          MAIL_FROM_NAME="dima63475@meta.ua",
                          MAIL_STARTTLS=False,
                          MAIL_SSL_TLS=True,
                          USE_CREDENTIALS=True,
                          VALIDATE_CERTS=True,
                          TEMPLATE_FOLDER=Path(__file__).parent/"templates")

@app.get("/")
def read_root():
    return {"message":"Hello dima"}

@app.post("/send_email")
async def send_email_background(background_tasks:BackgroundTasks,body:EmailSchema):
    message = MessageSchema(
        subject="Hello dima u recieve a sms from fastapi",
        recipients=[body.email],
        template_body={"fullname":"dima lisovyi"},
        subtype=MessageType.html)
    
    fm = FastMail(config)

    background_tasks.add_task(fm.send_message, message, template_name = "example_email.html")

    return {"message": "email has sent"}



































































