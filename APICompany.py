from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from typing import Optional
import metodAuth, columns, column_models
from typing import List

router = APIRouter(
    prefix='/auth',
    tags=['company']
)

user_dependency = Annotated[dict, Depends(metodAuth.get_current_user)]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/company/add", status_code=status.HTTP_201_CREATED)
async def create_company(u: user_dependency, company: column_models.CompanyBase, db: db_dependency):    
    db_company = columns.Companis(**company.dict())
    db.add(db_company)
    db.commit()

@router.get("/company/{name}", status_code=status.HTTP_200_OK, response_model=List[column_models.CompanyBase])
async def read_company_by_name(u: user_dependency, db: db_dependency, name: Optional[str] = None) -> List[column_models.CompanyBase]:    
    if name=='-':
        companis = db.query(columns.Companis).all()
    elif name:
        companis = db.query(columns.Companis).filter(columns.Companis.firm_name.like(f"%{name}%")).all()        

    if not companis:
        raise HTTPException(status_code=404, detail='companis not found')
    return [column_models.CompanyBase.from_orm(company) for company in companis]


@router.get("/company/{company_id}", status_code=status.HTTP_200_OK)
async def read_company_by_id(u: user_dependency, company_id:int, db: db_dependency):  
    company = db.query(columns.Companis).filter(columns.Companis.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail='Company not found')
    return company