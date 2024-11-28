from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
import metodAuth, columns
from typing import List

router = APIRouter(
    prefix='/auth',
    tags=['user']
)

user_dependency = Annotated[dict, Depends(metodAuth.get_current_user)]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(u: user_dependency, user_id: int, db: db_dependency):
    useraa = db.query(columns.Users).filter(columns.Users.id == user_id).first()
    if useraa is None:
        raise HTTPException(status_code=404, detail='User not found')
    return useraa

from typing import List

@router.get("/user/all", status_code=status.HTTP_200_OK, response_model=List[metodAuth.UserBase])
async def list_of_all_workers(u: user_dependency, db: db_dependency) -> List[metodAuth.UserBase]:
    workers = db.query(columns.Users).all()
    if not workers:
        raise HTTPException(status_code=404, detail="Workers are not found")
    return [metodAuth.UserBase.from_orm(worker) for worker in workers]