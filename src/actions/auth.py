from typing import Any, Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import redis
import pickle
from dotenv import load_dotenv
import os
from src.database.db import get_db
from src.actions import users as action
from src.conf.config import settings


class Auth:
    context = CryptContext(schemes=["bcrypt"],deprecated = "auto")
    SECRET = settings.secret
    AlGM = settings.algm
    oauth2 = OAuth2PasswordBearer(tokenUrl="/login")
    # r = redis.Redis(host="redis-141948-0.cloudclusters.net",port=11515,db=0,username="dima190179@gmail.com", password="VOxzVADCaKY-KSGLE5JFUFBQUFBQUFBQUFBQjFYQTB")

    def verify_password(self, ordinary_password, hashed_password):
        return self.context.verify(ordinary_password, hashed_password)
    
    def get_hash(self, ordinary_password):
        return self.context.hash(ordinary_password)
    
    async def create_accesstoken(self, data: dict, expires_time:Optional[float] = None):
        to_encode = data.copy()
        if expires_time:
            expire = datetime.utcnow() + timedelta(seconds=expires_time)
        else:
            expire = datetime.utcnow() + timedelta(minutes=200)
        to_encode.update({"iat":datetime.utcnow(), "exp":expire, "scope":"access_token"})
        encoded_token = jwt.encode(to_encode, self.SECRET, algorithm=self.AlGM)
        return encoded_token

    async def create_refreshtoken(self, data:dict, expires_time:Optional[float] = None):
        to_encode = data.copy()
        if expires_time:
            expire = datetime.utcnow() + timedelta(seconds=expires_time)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat":datetime.now(), "exp":expire, "scope":"refresh_token"})
        encoded_token = jwt.encode(to_encode, self.SECRET, algorithm=self.AlGM)
        return encoded_token
    

    async def decode_refresh(self, refresh_token:str):
        details = jwt.decode(refresh_token, self.SECRET, algorithms=self.AlGM)
        if details["scope"] == "refresh_token":
            email = details["sub"]
            return email
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= "invalid refresh token")
        

    async def get_user(self, token:str = Depends(oauth2), db: Session = Depends(get_db)):
        excpt = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cant validate iser", headers={"WWW":"Bearer"})
        data = jwt.decode(token, self.SECRET, algorithms=[self.AlGM])
        if data["scope"] == "access_token":
            email = data["sub"]
            if email is None:
                raise excpt

        # user = self.r.get(f"user:{email}")
        # if user is None:
        #     user = await action.get_user(email, db)
        #     if user is None:
        #         raise excpt
        #     self.r.set(f"user:{email}", pickle.dumps(user))
        #     self.r.expire(f"user:{email}",900)
        # else:
        #     user = pickle.loads(user)

        user = await action.get_user(email, db)
        if user is None:
            raise excpt

        return user
            

    async def create_email_token(self, data:dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat":datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET, algorithm=self.AlGM)
        return token
    
    async def get_email_fromToken(self,token:str):
        try:
            payload = jwt.decode(token, self.SECRET, algorithms=self.AlGM)
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
    
auth_user = Auth()