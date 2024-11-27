from fastapi import APIRouter, status
from database import db_dependency
from .models import UserBase, User
# from ..company import models

router = APIRouter()



# @router.post("/users/", status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserBase, db: db_dependency):    
#     db_user = User(**user.dict())
#     db.add(db_user)
#     db.commit()

# @router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
# async def read_user(user_id:int, db: db_dependency):  
#     user = db.query(User).filter(User.id == user_id).first
#     if user is None:
#         raise HttpException(status_code=404, detail='User not found')
#     return user