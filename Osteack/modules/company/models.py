


from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Enum, Integer, String, Text, Date, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class CompanyBase(BaseModel):
    firm_name: str  
    email: str
    phone: str | None  
    created_at: datetime

    class Config:
        orm_mode = True  


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firm_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), nullable=True)  
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


# class ConnectCompany(BaseModel):
#     worker_id: int  
#     company_id: int
#     next_meeting: datetime
#     is_approved: bool | False
#     status: bool | None
#     description: str | None
#     last_update: datetime
#     worker: User | None  
#     company: Company | None

#     class Config:
#         orm_mode = True  


# class ConnectCompany(Base):
#     __tablename__ = 'connect_companys'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     worker_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
#     company_id = Column(Integer, ForeignKey('company.id', ondelete='CASCADE'), nullable=False)
#     created_at = Column(TIMESTAMP, default=datetime.utcnow)
#     next_meeting = Column(DateTime, nullable=True)
#     is_approved = Column(Boolean, nullable=True)
#     status = Column(Enum('pending', 'completed', 'canceled', name='status_enum'), default='pending')
#     description = Column(Text, nullable=False)
#     last_update = Column(DateTime, nullable=True)

#     worker = relationship("User", backref="connect_companys")
#     company = relationship("Company", backref="connect_companys")