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
import authMethods

SESSION_TIME = 20

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY='1ca0b6d929bf74573d607d47244a4646b969806529c54e7ee1a02985d64e81f3a8890ccf45779f9cbf62c8fde16e27394c1f63f42911afe57d3b021bc81ece8d7374d86823ca1ee8000702c1a070084d6d2ea8ac6dccb47a4f1865db71e4723a6eb07c6d3534fd20dfffeb5d8a57a8ed2426a7519192f3acc26a90e517961598a700ab5ecc7fc2bbb0475e0315c3aa2e9f364f434d7b5b48b0e57899206a245caf2070981e534c85ca940df60bccb573b7750a9373f0ea5569a7868723392b55b200e752df98a7cb46e3ed160d7d97cac16fa667e97c7800f1524d52ac71e49972ee81f654d7f85b9b9a579f9466d25375641bdb4fe155c880d16f5bc812c421'
ALGORITHM='HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    full_name: str
    email: str
    last_date_connection: datetime | None  # Use native Python date type
    description: str | None
    updated_at: datetime    
    hashed_pass: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    city: str
    country: str
    phone_number: str   

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        full_name = create_user_request.full_name,
        email = create_user_request.email,
        description = create_user_request.description,
        updated_at = create_user_request.updated_at,
        hashed_pass = bcrypt_context.hash(create_user_request.hashed_pass), 
        last_date_connection=None,
        role_id=3
    )    
        
    db.add(create_user_model)
    db.commit()
    user_personal_details_model = PersonalDetails(
        user_id=create_user_model.id,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        date_of_birth=create_user_request.date_of_birth,
        city=create_user_request.city,
        country=create_user_request.country,
        phone_number=create_user_request.phone_number
    )
    db.add(user_personal_details_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(from_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                  db: db_dependency):
    user = authMethods.authenticate_user(from_data.username, from_data.password, db)  # Use username here
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )
    token = authMethods.create_access_token(user, timedelta(minutes=SESSION_TIME))
    return {"access_token": token, "token_type": "bearer"}


    

    


