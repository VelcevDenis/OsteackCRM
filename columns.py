from enum import Enum
from sqlalchemy import Boolean, Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum as SQLAlchemyEnum, TIMESTAMP  # Correct Enum import from sqlalchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False)  

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)    
    last_date_connection = Column(Date, nullable=True)
    is_deleted = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE', onupdate='CASCADE'))
    hashed_pass = Column(Text, nullable=False)
    role = relationship("Roles", backref="users")

class PersonalDetails(Base):
    __tablename__ = 'personal_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    phone_number = Column(String(15), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("Users", backref="personal_details")


class Companis(Base):
    __tablename__ = 'companis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firm_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), nullable=True)  
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class StatusEnum(str, Enum):
    pending = 'pending'
    completed = 'completed'
    canceled = 'canceled'
    waiting = 'waiting'

class ConnectCompanis(Base):
    __tablename__ = 'connect_companis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    company_id = Column(Integer, ForeignKey('companis.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    next_meeting = Column(DateTime, nullable=True)
    is_approved = Column(Boolean, nullable=True)
    status = Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.pending)
    description = Column(Text, nullable=False)
    last_update = Column(DateTime, nullable=True)

    worker = relationship("Users", backref="connect_companis")
    company = relationship("Companis", backref="connect_companis")