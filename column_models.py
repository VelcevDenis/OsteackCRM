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

class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # Use this instead of orm_mode

class CategoryBaseCreateUpdate(BaseModel):
    name: str

    class Config:
        from_attributes = True  # Use this instead of orm_mode

class SubCategoryBase(BaseModel):
    id: int
    name: str
    count:int
    category_id: int

    class Config:
        from_attributes = True

class SubCategoryCreateBase(BaseModel):
    name: str
    count:int
    length: int
    width: int
    height: int
    price_per_piece:float
    booked:Optional[int] = None
    category_id: int

    class Config:
        from_attributes = True

class SubCategoryBaseUpdate(BaseModel):
    name: str
    count:int 
    length: int
    width: int
    height: int
    price_per_piece:float
    booked:Optional[int] = None
    class Config:
        from_attributes = True

# class SubCategoryBaseUpdate(BaseModel):
#     id: int
#     booked:Optional[int] = None
#     class Config:
#         from_attributes = True

class ProductBase(BaseModel):
    id: int
    customer_name: str
    count: int
    length: int
    width: int
    height: int
    total_price: Optional[float] = None
    description: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    last_update: Optional[datetime] = None
    status: columns.StatusEnum = columns.StatusEnum.pending
    category_id: int
    sub_category_id: int
    category_obj: Optional[CategoryBase] = None
    sub_category_obj: Optional[SubCategoryBase] = None

    class Config:
        from_attributes = True

class ProductCreateBase(BaseModel):
    customer_name: str
    count: int
    length: int
    width: int
    height: int
    total_price: Optional[float] = None
    description: Optional[str] = None
    category_id: int
    sub_category_id: int

    class Config:
        from_attributes = True


# class HistoryProductBase(BaseModel):
#     id: int
#     name: str
#     procent: int
#     price: int
#     final_price: int
#     product_count: int
#     status: columns.StatusEnum = columns.StatusEnum.pending

#     class Config:
#         from_attributes = True

# class EditHistoryProductBase(BaseModel):    
#     status: columns.StatusEnum = columns.StatusEnum.pending

#     class Config:
#         from_attributes = True