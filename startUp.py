from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import  Date, DateTime
from pydantic import BaseModel
from typing import Annotated
import models
from datetime import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import relationship, Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    try:
        db: Session = next(get_db()) 
        roles = ['SuperAdmin', 'Admin', 'Worker']
        for role_name in roles:
            role = models.Roles(role_name=role_name)
            existing_role = db.query(models.Roles).filter(models.Roles.role_name == role_name).first()
            if not existing_role:
                db.add(role)
        db.commit()  # Commit once after adding roles to reduce database operations

        super_admin_role = db.query(models.Roles).filter(models.Roles.role_name == "SuperAdmin").first()
        if super_admin_role:
            existing_user = db.query(models.Users).filter(models.Users.email == "denisv@ost.com").first()
            if not existing_user:
                user = models.Users(
                    full_name="Den V",
                    email="denisv@ost.com",
                    last_date_connection=datetime(2024, 11, 16),
                    description="Leading tech firm",
                    hashed_pass = "Test123!",
                    role_id=super_admin_role.id
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                print(f"User {user.full_name} created successfully.")
            else:
                print("User already exists.")

            existing_personal_detail = db.query(models.PersonalDetails).filter(models.PersonalDetails.user_id == user.id).first()
            if not existing_personal_detail:
                personal_detail = models.PersonalDetails(
                    user_id=user.id,
                    first_name='Den',
                    last_name='V',
                    date_of_birth=datetime(1990, 5, 20),
                    city='San Francisco',
                    country='USA',
                    phone_number='+123456789'
                )
                db.add(personal_detail)
                db.commit()
                db.refresh(personal_detail)
                print(f"PersonalDetail for user {user.full_name} created successfully.")
            else:
                print("PersonalDetail for user already exists.")

        # Insert the company if it doesn't exist
        existing_company = db.query(models.Companis).filter(models.Companis.email == 'contact@techinnovators.com').first()
        if not existing_company:
            company = models.Companis(
                firm_name='Tech Innovators Inc.',
                email='contact@techinnovators.com',
                phone='+987654321'
            )
            db.add(company)
            db.commit()
            db.refresh(company)
            print(f"Company {company.firm_name} created successfully.")
        else:
            company = existing_company
            print("Company already exists.")

        # Insert the ConnectCompany if it doesn't exist
        existing_connect_company = db.query(models.ConnectCompanis).filter(
            models.ConnectCompanis.worker_id == user.id,
            models.ConnectCompanis.company_id == company.id
        ).first()
        
        if not existing_connect_company:
            connect_company = models.ConnectCompanis(
                worker_id=user.id,
                company_id=company.id,
                next_meeting=datetime(2024, 11, 25, 14, 30),
                is_approved=False,
                status=None,
                description='Discussing the integration project',
                last_update=datetime(2024, 11, 20)
            )
            db.add(connect_company)
            db.commit()
            db.refresh(connect_company)
            print(f"ConnectCompany between user {user.full_name} and company {company.firm_name} created successfully.")
        else:
            print("ConnectCompany already exists between the user and company.")
    except Exception as e:
        print(f"Error during startup: {e}")
        db.rollback()
    

class RoleBase(BaseModel):
    role_name: str

    class Config:
        orm_mode = True 

class UserBase(BaseModel):
    full_name: str
    email: str
    last_date_connection: datetime | None  # Use native Python date type
    is_deleted: bool
    description: str | None
    updated_at: datetime
    role_id: int
    hashed_pass: str

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

class ConnectCompanyBase(BaseModel):
    worker_id: int  
    company_id: int
    next_meeting: datetime
    is_approved: bool
    status: bool | None
    description: str | None
    last_update: datetime

    class Config:
        orm_mode = True 

