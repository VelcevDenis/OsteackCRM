from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from datetime import timedelta, datetime
from pydantic import BaseModel, Field
import columns
from auth import metod as mAuth
from typing import List

router = APIRouter(
    prefix='/auth',
    tags=['user']
)

user_dependency = Annotated[dict, Depends(mAuth.get_current_user)]

class SearchUserRequest(BaseModel):
    userId: int | None = None
    first_name: str  
    last_name: str 
    email: str
    phone: str | None  
    created_at: datetime
    description: str | None
    last_date_connection: datetime | None = None
    role: str
    country: str
    city: str
    date_of_birth: datetime | None


class EditUserRequest(BaseModel): 
    first_name: str = Field(required=None)  
    last_name: str 
    email: str
    phone: str | None
    description: str | None
    role_id: int
    country: str
    city: str
    date_of_birth: datetime | None    
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/users/by-id/{userId}", status_code=status.HTTP_200_OK)
async def read_user(u: user_dependency, userId: int, db: db_dependency):
    useraa = db.query(columns.Users).filter(columns.Users.id == userId).first()
    if useraa is None:
        raise HTTPException(status_code=404, detail='User not found')
    return useraa

from typing import List

@router.get("/user/all", response_model=List[SearchUserRequest])
async def list_of_all_employees(u: user_dependency, db: db_dependency, skip: int = 0, limit: int = 5):    
    employees = db.query(columns.Users, columns.PersonalDetails, columns.Roles
                        ).join(columns.PersonalDetails, columns.PersonalDetails.user_id == columns.Users.id
                        ).join(columns.Roles, columns.Users.role_id == columns.Roles.id
                        ).offset(skip).limit(limit).all()
    
    result = [
    SearchUserRequest(
        userId=user.id,
        first_name=personal_det.first_name,
        last_name=personal_det.last_name,
        email=user.email,
        phone=personal_det.phone_number,
        created_at=personal_det.created_at,
        description=user.description,
        last_date_connection=user.last_date_connection,
        role=role.role_name,
        country=personal_det.country,
        city=personal_det.city,
        date_of_birth=personal_det.date_of_birth
    )
    for user, personal_det, role in employees
]
    
    return result


@router.put("/user/edit/{userId}", status_code=status.HTTP_200_OK)
async def edit_user(u: user_dependency, db: db_dependency, userId: int, editUserRequest: EditUserRequest):   
    user_model = db.query(columns.Users).filter(columns.Users.id == userId).first()
    
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Connect user with id {userId} not found"
        )    
    
    user_model.full_name = f"{editUserRequest.first_name} {editUserRequest.last_name}"
    user_model.email = editUserRequest.email
    user_model.description = editUserRequest.description   
    user_model.role_id = editUserRequest.role_id 
    user_model.last_update = datetime.utcnow()  
    db.commit()

    personal_det = db.query(columns.PersonalDetails).filter(columns.PersonalDetails.user_id == userId).first()

    personal_det.phone_number = editUserRequest.phone
    personal_det.country = editUserRequest.country
    personal_det.city = editUserRequest.city
    personal_det.date_of_birth = editUserRequest.date_of_birth
    db.commit()

    return {"message": "Connect user updated successfully"}  