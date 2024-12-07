from typing import Annotated
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette import status
from database import SessionLocal
from typing import Optional
import metodAuth, columns, column_models
from typing import List

router = APIRouter(
    prefix='/auth',
    tags=['recallCompany']
)

user_dependency = Annotated[dict, Depends(metodAuth.get_current_user)]

class CreateConnectCompanyRequest(BaseModel):
    company_id:int
    next_meeting: datetime | None
    is_approved: bool
    status: columns.StatusEnum = columns.StatusEnum.pending  
    description:str | None       

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/recallCompanis/add", status_code=status.HTTP_201_CREATED)
async def create_connectCompany(u: user_dependency, db: db_dependency, connectCompany: CreateConnectCompanyRequest):    
    create_connect_company_model = columns.ConnectCompanis(
        worker_id = u.get('id'),
        company_id = connectCompany.company_id,
        created_at = datetime.utcnow(),
        next_meeting = connectCompany.next_meeting,
        is_approved = 0,
        status = connectCompany.status,
        description = connectCompany.description
    )    

    db.add(create_connect_company_model)
    db.commit()

@router.get("/recallCompanis/by-pt-id{connectCompany_id}", status_code=status.HTTP_200_OK)
async def read_connectCompany(u: user_dependency, connectCompany_id:int, db: db_dependency):  
    connectCompany = db.query(columns.ConnectCompanis).filter(columns.ConnectCompanis.id == connectCompany_id).first()
    if connectCompany is None:
        raise HTTPException(status_code=404, detail='Company Contact not found')
    return connectCompany

@router.get("/recallCompanis/by-worker-id/{worker_id}", status_code=status.HTTP_200_OK, response_model=List[column_models.ConnectCompanyBase])
async def read_connect_company_by_name(u: user_dependency, db: db_dependency, worker_id: int) -> List[column_models.ConnectCompanyBase]:    
    # if worker_id == 10000000:
    #     companis = db.query(columns.ConnectCompanis).all()
    if worker_id:
        companis = db.query(columns.ConnectCompanis).filter(columns.ConnectCompanis.worker_id == worker_id).all()

    return [column_models.CompanyBase.from_orm(company) for company in companis]


@router.get("/potentialCompanies/all", response_model=List[column_models.ConnectCompanyBase])
async def list_of_all_potential_companis(u: user_dependency, db: db_dependency, skip:int=0, limit:int=100):
    potential_clients = db.query(columns.ConnectCompanis).offset(skip).limit(limit).all()
    return potential_clients