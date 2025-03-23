from enum import Enum
from sqlalchemy import Float, Boolean, Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum as SQLAlchemyEnum, TIMESTAMP  # Correct Enum import from sqlalchemy
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

class ConnectCompanis(Base):
    __tablename__ = 'connect_companis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    company_id = Column(Integer, ForeignKey('companis.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    next_meeting = Column(DateTime, nullable=True)
    is_approved = Column(Boolean, nullable=True)
    status = Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.pending)
    description = Column(Text, nullable=True)
    last_update = Column(DateTime, nullable=True)

    worker = relationship("Users", backref="connect_companis")
    company = relationship("Companis", backref="connect_companis")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False) 

class SubCategory(Base):
    __tablename__ = "sub_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    count = Column(Integer, nullable=False, default=0)
    booked = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))  # Add this foreign key

    category = relationship("Category", backref="sub_categories")  # Fix backref name

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    count = Column(Integer, nullable=False, default=0)
    length = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False) 
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    last_update = Column(DateTime, nullable=True)  
    status = Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.pending)

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    sub_category_id = Column(Integer, ForeignKey("sub_categories.id", ondelete="CASCADE"))

    category = relationship("Category", backref="products")
    sub_category = relationship("SubCategory", backref="products")


# class HistoryProduct(Base):
#     __tablename__ = "history_product"
#     id = Column(Integer, primary_key=True, index=True)
#     product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
#     procent = Column(Integer, nullable=False)
#     price = Column(Integer, nullable=False)
#     final_price = Column(Integer, nullable=False)
#     product_count = Column(Integer, nullable=False)
#     status = Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.pending)

#     product = relationship("Product", backref="history_products")


