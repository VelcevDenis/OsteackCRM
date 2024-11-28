from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import  Date, DateTime
from pydantic import BaseModel
from typing import Annotated
import columns
from datetime import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import relationship, Session
import APIAuth, metodAuth, startUp


app = FastAPI()
app.include_router(APIAuth.router)

columns.Base.metadata.create_all(bind=engine)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(metodAuth.get_current_user)]

startUp.startup()


#REGION controller methods

# @app.get("/roles/", status_code=status.HTTP_200_OK)
# async def get_all_roles(db: Session = Depends(get_db)):
#     roles = db.query(models.Roles).all()  

# @app.post("/role/", status_code=status.HTTP_201_CREATED)
# async def create_role(role: RoleBase, db: db_dependency):
#     db_role = models.Roles(**role.dict())
#     db.add(db_role)
#     db.commit()
#     db.refresh(db_role)
#     return db_role

# @app.get("/role/{role_id}", status_code=status.HTTP_200_OK)
# async def read_user(role_id:int, db: db_dependency):  
#     role = db.query(models.Roles).filter(models.Roles.id == role_id).first
#     if role is None:
#         raise HTTPException(status_code=404, detail='Role not found')
#     return role













# @app.post("/compani/", status_code=status.HTTP_201_CREATED)
# async def create_company(company: CompanyBase, db: db_dependency):    
#     db_company = models.Companis(**company.dict())
#     db.add(db_company)
#     db.commit()

# @app.get("/compani/{company_id}", status_code=status.HTTP_200_OK)
# async def read_company(company_id:int, db: db_dependency):  
#     company = db.query(models.Companis).filter(models.Companis.id == company_id).first
#     if company is None:
#         raise HTTPException(status_code=404, detail='Company not found')
#     return company


# @app.post("/connectCompany/", status_code=status.HTTP_201_CREATED)
# async def create_connectCompany(connectCompany: ConnectCompanyBase, db: db_dependency):    
#     db_connectCompany = models.ConnectCompanis(**connectCompany.dict())
#     db.add(db_connectCompany)
#     db.commit()

# @app.get("/connectCompany/{connectCompany_id}", status_code=status.HTTP_200_OK)
# async def read_connectCompany(connectCompany_id:int, db: db_dependency):  
#     connectCompany = db.query(models.ConnectCompanis).filter(models.ConnectCompanis.id == connectCompany_id).first
#     if connectCompany is None:
#         raise HTTPException(status_code=404, detail='Company Contact not found')
#     return connectCompany