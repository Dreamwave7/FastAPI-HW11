from pathlib import Path

from fastapi_mail import FastMail, ConnectionConfig,MessageSchema, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.actions.auth import auth_user

config = ConnectionConfig(MAIL_USERNAME="dima63475@meta.ua",
                          MAIL_PASSWORD="Zazazadima19017901",
                          MAIL_PORT=465,
                          MAIL_SERVER="smtp.meta.ua",
                          MAIL_STARTTLS=False,
                          MAIL_SSL_TLS=True,
                          MAIL_FROM="dima63475@meta.ua",
                          MAIL_FROM_NAME="KingKong",
                          TEMPLATE_FOLDER=Path(__file__).parent / "templates",
                          USE_CREDENTIALS=True)

async def send_email(email:EmailStr, username:str, host:str):
    try:
        
        token_verification = auth_user.create_email_token({"sub":email})
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={"host":host, "username":username,"token":token_verification},
            subtype=MessageType.html
            )
        
        fm = FastMail(config)
        await fm.send_message(message, template_name="example_email.html")

    except ConnectionError as e:
        print(e)