from pydantic import BaseModel
from database import Base
from sqlalchemy import Boolean, Column, Integer, String, Text, Date, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime


from datetime import date

class UserBase(BaseModel):
    full_name: str
    email: str
    phone: str
    last_date_connection: date | None  # Use native Python date type
    is_deleted: bool
    description: str | None
    updated_at: datetime
    role_id: int


# SQLAlchemy Model for Database Representation
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), nullable=True)
    last_date_connection = Column(Date, nullable=True)
    is_deleted = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    role = relationship("Role", backref="users")


# Uncomment and correct the following models if needed
# class PersonalDetailBase(BaseModel):
#     user_id: int
#     first_name: str
#     last_name: str
#     date_of_birth: Date
#     city: str
#     country: str
#     phone_number: str
#     created_at: datetime
#     updated_at: datetime


# class PersonalDetail(Base):
#     __tablename__ = 'personal_details'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String(50), nullable=False)
#     date_of_birth = Column(Date, nullable=False)
#     city = Column(String(100), nullable=True)
#     country = Column(String(100), nullable=True)
#     phone_number = Column(String(15), nullable=True)
#     created_at = Column(TIMESTAMP, default=datetime.utcnow)
#     updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

#     user = relationship("User", backref="personal_details")
