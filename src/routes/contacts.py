from typing import List
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status
from src.database.db import get_db
from src.schemas import *
from src.actions import contacts as act
from src.actions import users as user_act
from src.actions.auth import auth_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/contacts")
security = HTTPBearer()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, db:Session = Depends(get_db)):
    exist_user = await user_act.get_user(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="account already exist")
    body.password = auth_user.get_hash(body.password)
    new_user = await user_act.create_user(body, db)
    return {"user":new_user, "detail": "user created!"}

@router.post("/login",response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = await user_act.get_user(body.username, db)
    
    return "d"


# @router.post("/create")
# async def create_contact(body: ContactModel, db:Session = Depends(get_db)):
#     res = await con.create_new_contact(body, db)
#     return res

# @router.get("/", response_model=List[ContactModel])
# async def contacts(db :Session = Depends(get_db)):
#     res = await con.get_contacts(db)
#     return res


# @router.get("/birthdays", response_model=List[ContactModel])
# async def get_birthdays(db:Session = Depends(get_db)):
#     res = await con.birthdays_7(db)
#     return res


# @router.get("/{contact_id}")
# async def read_note(contact_id:int, db:Session = Depends(get_db)):
#     res = await con.get_contact(contact_id, db)
#     return res


# @router.patch("/change")
# async def change(body:ContactUpdate, db:Session = Depends(get_db)):
#     res = await con.change_contact(body, db)
#     return res

# @router.delete("/delete")
# async def delete(name:ContactName, db:Session = Depends(get_db)):
#     res = await con.delete(name, db)
#     return res

# @router.post("/find/name")
# async def search_name(username:ContactName, db:Session = Depends(get_db)):
#     res = await con.find_name(username, db)
#     return res


# @router.post("/find/birthday", response_model= List[ContactModel])
# async def search_birthday(birthday:ContactBirthday, db:Session = Depends(get_db)):
#     res = await con.find_birthday(birthday, db)
#     return res

# @router.post("/find/lastname", response_model= List[ContactModel])
# async def search_lastname(lastname:ContactLastname, db: Session = Depends(get_db)):
#     res = await con.find_lastname(lastname, db)
#     return res

# @router.get("/birthdays")
# async def get_birthdays(db:Session = Depends(get_db)):
#     res = await con.birthdays_7(db)
#     return res