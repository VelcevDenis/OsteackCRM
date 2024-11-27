from fastapi import APIRouter, status  
from database import db_dependency
from .models import RoleBase, Role
# from ..company import models

router = APIRouter()

# @router.post("/roles/", status_code=status.HTTP_201_CREATED)
# async def create_role(role: RoleBase, db: db_dependency):    
#     db_role = Role(**role.dict())
#     db.add(db_role)
#     db.commit()

# @router.get("/roles/{role_id}", status_code=status.HTTP_200_OK)
# async def read_role(role:int, db: db_dependency):  
#     role = db.query(Role).filter(Role.id == role_id).first
#     if role is None:
#         raise HttpException(status_code=404, detail='Role not found')
#     return role