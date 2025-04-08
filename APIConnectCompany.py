from typing import Annotated
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette import status
from database import SessionLocal
from typing import Optional
import columns, column_models
from auth import metod as mAuth
from typing import List

router = APIRouter(
    prefix='/auth',
    tags=['recallCompany']
)

user_dependency = Annotated[dict, Depends(mAuth.get_current_user)]

class CreateConnectCompanyRequest(BaseModel):  
    company_id: int | None = None
    firm_name: str  
    email: str
    phone: str | None  
    next_meeting: datetime | None
    is_approved: bool
    status: columns.StatusEnum = columns.StatusEnum.pending  
    description: str | None
    last_update: datetime | None = None

class EditConnectCompanyRequest(BaseModel): 
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
    create_company_model = columns.Companis(
        firm_name=connectCompany.firm_name,  
        email=connectCompany.email,
        phone=connectCompany.phone,
        created_at=datetime.utcnow()
    )            
    db.add(create_company_model)
    db.commit()
    db.refresh(create_company_model)
    
    create_connect_company_model = columns.ConnectCompanis(
        worker_id=u.get('id'),
        company_id=create_company_model.id,
        created_at=datetime.utcnow(),
        next_meeting=connectCompany.next_meeting,
        is_approved=0,
        status=connectCompany.status,
        description=connectCompany.description
    )    

    db.add(create_connect_company_model)
    db.commit()
    return {"message": "Company and connection created successfully."}


@router.get("/recallCompanis/by-pt-id{connectCompany_id}", status_code=status.HTTP_200_OK)
async def read_connectCompany(u: user_dependency, connectCompany_id:int, db: db_dependency):  
    connectCompany = db.query(columns.ConnectCompanis).filter(columns.ConnectCompanis.id == connectCompany_id).first()
    if connectCompany is None:
        raise HTTPException(status_code=404, detail='Company Contact not found')
    return connectCompany

@router.get("/recallCompanis/by-worker-id/{worker_id}", status_code=status.HTTP_200_OK, response_model=List[column_models.ConnectCompanyBase])
async def read_connect_company_by_name(u: user_dependency, db: db_dependency, worker_id: int) -> List[column_models.ConnectCompanyBase]:
    if worker_id:
        companis = db.query(columns.ConnectCompanis).filter(columns.ConnectCompanis.worker_id == worker_id).all()

    return [column_models.CompanyBase.from_orm(company) for company in companis]


@router.get("/potentialCompanies/all", response_model=List[CreateConnectCompanyRequest])
async def list_of_all_potential_companis(u: user_dependency, db: db_dependency, skip: int = 0, limit: int = 5):
    potential_clients = db.query(columns.ConnectCompanis).join(
        columns.Companis, columns.ConnectCompanis.company_id == columns.Companis.id
    ).offset(skip).limit(limit).all()
    
    # ///// filter by worker_id
    # potential_clients = db.query(columns.ConnectCompanis).join(
    #     columns.Companis, columns.ConnectCompanis.company_id == columns.Companis.id
    # ).filter(columns.ConnectCompanis.worker_id == u.get('id')).offset(skip).limit(limit).all()
    
    result = [
        CreateConnectCompanyRequest(
            company_id = client.company.id,
            firm_name=client.company.firm_name,
            email=client.company.email,
            phone=client.company.phone,
            next_meeting=client.next_meeting,
            is_approved=client.is_approved,
            status=client.status,
            description=client.description,
            last_update=client.last_update
        )
        for client in potential_clients
    ]
    
    return result

@router.put("/recallCompanis/edit/{connect_company_id}", status_code=status.HTTP_200_OK)
async def edit_connect_company(u: user_dependency, db: db_dependency, connect_company_id: int, connectCompany: EditConnectCompanyRequest):   
    connect_company_model = db.query(columns.ConnectCompanis).filter(columns.ConnectCompanis.company_id == connect_company_id).first()
    if not connect_company_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Connect company with id {connect_company_id} not found"
        )
    
    connect_company_model.next_meeting = connectCompany.next_meeting
    connect_company_model.status = connectCompany.status
    connect_company_model.description = connectCompany.description
    connect_company_model.is_approved = 0 if connectCompany.status == columns.StatusEnum.pending else connect_company_model.is_approved  
    connect_company_model.last_update = datetime.utcnow()  

    db.commit()

    return {"message": "Connect company updated successfully"}