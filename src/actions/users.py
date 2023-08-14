from sqlalchemy.orm import Session
from src.database.models import *
from src.schemas import *


async def get_user(email:str, db:Session):
    return db.query(User).filter(User.email == email).first()
 
async def create_user(body: UserModel, db: Session):
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def refresh_token(user: User, token:str, db: Session):
    user.refresh_token = token
    db.commit()
    return "Done"

async def update_token(user:User, db:Session, token:str):
    user.refresh_token = token
    db.commit()
    db.refresh(user)
    return "done"