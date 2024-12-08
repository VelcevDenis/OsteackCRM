from sqlalchemy import  Date, DateTime
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import columns

class RoleBase(BaseModel):
    role_name: str

    class Config:
        orm_mode = True 

class PersonalDetailBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    date_of_birth: Date
    city: str
    country: str
    phone_number: str
    created_at: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class CompanyBase(BaseModel):
    firm_name: str  
    email: str
    phone: str | None  
    created_at: datetime 

    class Config:
        orm_mode = True
        from_attributes = True

class ConnectCompanyBase(BaseModel):
    worker_id: int  
    company_id: int
    next_meeting: datetime
    is_approved: bool
    status: columns.StatusEnum = columns.StatusEnum.pending 
    description: Optional[str] = None  # Make description optional
    last_update: Optional[datetime] = None  # Make last_update optional

    class Config:
        orm_mode = True 
        from_attributes = True