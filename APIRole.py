from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
import metodAuth, columns, column_models
from typing import List

router = APIRouter(
    prefix='/auth',
    tags=['role']
)

user_dependency = Annotated[dict, Depends(metodAuth.get_current_user)]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/roles/", status_code=status.HTTP_200_OK, response_model=List[column_models.RoleBase])
async def get_all_roles(u: user_dependency, db: Session = Depends(get_db)):
    roles = db.query(columns.Roles).all()     
    if not roles:
        raise HTTPException(status_code=404, detail="Roles are not found")
    return roles

@router.post("/role/", status_code=status.HTTP_201_CREATED)
async def create_role(u: user_dependency, role: column_models.RoleBase, db: db_dependency):
    db_role = columns.Roles(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/role/{role_id}", status_code=status.HTTP_200_OK, response_model=column_models.RoleBase)
async def read_user(u: user_dependency, role_id:int, db: db_dependency):  
    role = db.query(columns.Roles).filter(columns.Roles.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail='Role not found')
    return role