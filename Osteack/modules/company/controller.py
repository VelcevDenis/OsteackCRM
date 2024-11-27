from fastapi import APIRouter, status  
from database import db_dependency
from .models import CompanyBase, Company
# from ..company import models

router = APIRouter()

@router.post("/companis/", status_code=status.HTTP_201_CREATED)
async def create_company(company: CompanyBase, db: db_dependency):    
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()

@router.get("/companis/{company_id}", status_code=status.HTTP_200_OK)
async def read_company(company_id:int, db: db_dependency):  
    company = db.query(Company).filter(Company.id == company_id).first
    if company is None:
        raise HttpException(status_code=404, detail='Company not found')
    return company