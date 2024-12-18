from datetime import timedelta, datetime, date
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from columns import Users, PersonalDetails
from fastapi.security import OAuth2PasswordRequestForm
import metodAuth
from config import settings


SESSION_TIME = settings.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
 
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

user_dependency = Annotated[dict, Depends(metodAuth.get_current_user)]

class CreateUserRequest(BaseModel):    
    email: str
    last_date_connection: datetime | None = None
    description: str | None 
    hashed_pass: str
    first_name: str
    last_name: str
    date_of_birth: date | None = None
    city: str
    country: str
    phone: str 
    role_id:int = 3  

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


@router.post("/employee/add", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        full_name = f"{create_user_request.first_name} {create_user_request.last_name}",
        email = create_user_request.email,
        description = create_user_request.description,
        hashed_pass = metodAuth.bcrypt_context.hash(create_user_request.hashed_pass),         
        role_id= create_user_request.role_id
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
        phone_number=create_user_request.phone
    )
    db.add(user_personal_details_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(from_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                  db: db_dependency):
    user = metodAuth.authenticate_user(from_data.username, from_data.password, db)  # Use username here
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )
    token = metodAuth.create_access_token(user, timedelta(minutes=SESSION_TIME))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/verify-token/{token}")
async def auth_user_token_verification(token:str):
    info = await metodAuth.get_current_user(token=token)
    return {"info":info}