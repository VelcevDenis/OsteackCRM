from datetime import timedelta, datetime
from sqlalchemy import  Date
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users, PersonalDetails
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

SECRET_KEY='cd194d468c42e20869646e5701346662ca428dde39f03d97303616724efbdb5f501cd8f36b00043adb185ae4b861a9aba49c9b5e460d177f90d76d5acb353a28357779105e796773b41eb682fd9d3f3609d9cbead548f9e3e679840b078aa1aeaa6c11e203df410fc2914e915f4dbdfe781b688e9d3ee5e63680ac8fdb4b437391ae43adabf118a4fb899ead206f18d8cde2ad3722ec58c1cd4329675579055100d2657c59c6241bef2fe9767cc8bfde0b06685ffd4ee4137ecf3ed00c03fb333aac0639cccfc5e159657944cb1789b5895efb64a4c3bad180e6cd630baba87bbf075a9333f66f55300a7d239def04b9a3860bf4a85032559d7c2251c6c57e3f'
ALGORITHM='HS265'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str= payload.get('email')
        user_id: int = payload.get('id')
        role: int = payload.get('role')
        if email is None or user_id is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Counld not validate user.')
        return {'email':email, 'id':user_id, 'role': role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')