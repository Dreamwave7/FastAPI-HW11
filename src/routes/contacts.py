from typing import List
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status, Security
from src.database.db import get_db
from src.schemas import *
from src.actions import contacts as act
from src.actions import users as user_act
from src.actions.auth import auth_user
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks, Request
from src.actions.email import send_email

router = APIRouter(prefix="/contacts")
security = HTTPBearer()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel,back_tasks: BackgroundTasks,request:Request, db:Session = Depends(get_db)):
    exist_user = await user_act.get_user(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="account already exist")
    body.password = auth_user.get_hash(body.password)
    new_user = await user_act.create_user(body, db)
    back_tasks.add_task(send_email, new_user.email, new_user.username,request.base_url)
    return {"user":new_user, "detail": "user created! \n Check Your email for verification!"}

@router.post("/login",response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = await user_act.get_user(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email")
    if not auth_user.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" invalid password")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="  user not confirmed")


    access_token = await auth_user.create_accesstoken(data={"sub":user.email})
    refresh_token = await auth_user.create_refreshtoken(data={"sub":user.email})
    await user_act.update_token(user,db, refresh_token)
    return {"access_token":access_token, "refresh_token":refresh_token,"token_type":"bearer"}

@router.post("/refresh_token",response_model=TokenModel)
async def refresh_token(info:HTTPAuthorizationCredentials = Security(security), db:Session = Depends(get_db)):
    token = info.credentials
    email = await auth_user.decode_refresh(token)
    user = await user_act.get_user(email,db)
    if user.refresh_token != token:
        await user_act.update_token(user,db,None)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" invalid email")
    access = await auth_user.create_accesstoken(data={"sub":email})
    refresh = await auth_user.create_refreshtoken(data={"sub":email})
    await user_act.update_token(user,db,token)

    return {"access_token":access, "refresh_token":refresh, "token_type":"bearer"}


@router.get("/confirmed_email/{token}")
async def confirm_email(token:str, db:Session = Depends(get_db)):
    email = await auth_user.get_email_fromToken(token)
    user = await user_act.get_user(email,db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="verification error")
    if user.confirmed:
        return {"message":"your email is already confirmed"}
    
    await user_act.confirm_email(email,db)
    return {"message": "email confirmed"}

@router.post("/test_access")
async def test_access(user:User = Depends(auth_user.get_user)):
    return {"user":user.email}



#Action with contacts

@router.post("/create")
async def create_contact(body: ContactModel,user: User = Depends(auth_user.get_user), db:Session = Depends(get_db)):
    new_contact = await act.create_new_contact(body, user, db)
    return {"new_contact_created":new_contact}

@router.post("/get_contacts",response_model=List[ContactResponse])
async def contacts(user:User = Depends(auth_user.get_user),db :Session = Depends(get_db)):
    res = await act.get_contacts(user,db)
    return res


@router.post("/get_contact/{contact_id}",response_model=ContactResponse)
async def read_note(contact_id:int,user:User = Depends(auth_user.get_user), db:Session = Depends(get_db)):
    res = await act.get_contact(contact_id, user, db)
    return res



@router.post("/birthdays", response_model=List[ContactResponse])
async def get_birthdays(user:User= Depends(auth_user.get_user),db:Session = Depends(get_db)):
    res = await act.birthdays_7(user,db)
    return res


@router.delete("/delete/{contact_id}",response_model=ContactResponse)
async def delete(contact_id, user:User =Depends(auth_user.get_user),db:Session = Depends(get_db)):
    res = await act.delete_contact(contact_id,user,db)
    return res



@router.patch("/change")
async def change(body:ContactUpdate,contact_id:int, user :User = Depends(auth_user.get_user), db:Session = Depends(get_db)):
    res = await act.change_contact(body,contact_id, db)
    return res


@router.post("/request_email")
async def request_email(body:RequestEmail, back_task:BackgroundTasks, request:Request, db:Session = Depends(get_db)):
    user = await user_act.get_user(body.email, db)

    if user.confirmed:
        return {"message": "Check your email for confirmation."}



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

