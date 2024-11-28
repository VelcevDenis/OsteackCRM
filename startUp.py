from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import  Date, DateTime
from pydantic import BaseModel
from typing import Annotated
from datetime import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import relationship, Session
import columns
import APIAuth, metodAuth


app = FastAPI()
app.include_router(APIAuth.router)

columns.Base.metadata.create_all(bind=engine)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(metodAuth.get_current_user)]

@app.on_event("startup")
def startup():
    try:
        db: Session = next(get_db()) 
        roles = ['SuperAdmin', 'Admin', 'Worker']
        for role_name in roles:
            role = columns.Roles(role_name=role_name)
            existing_role = db.query(columns.Roles).filter(columns.Roles.role_name == role_name).first()
            if not existing_role:
                db.add(role)
        db.commit()  # Commit once after adding roles to reduce database operations

        super_admin_role = db.query(columns.Roles).filter(columns.Roles.role_name == "SuperAdmin").first()
        if super_admin_role:
            existing_user = db.query(columns.Users).filter(columns.Users.email == "denisv@ost.com").first()
            if not existing_user:
                user = columns.Users(
                    full_name="Den V",
                    email="sa@ost.com",
                    last_date_connection=datetime(2024, 11, 16),
                    description="Leading tech firm",
                    hashed_pass = metodAuth.bcrypt_context.hash("Test123!"),
                    role_id=super_admin_role.id
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                print(f"User {user.full_name} created successfully.")
            else:
                print("User already exists.")

            existing_personal_detail = db.query(columns.PersonalDetails).filter(columns.PersonalDetails.user_id == user.id).first()
            if not existing_personal_detail:
                personal_detail = columns.PersonalDetails(
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
        existing_company = db.query(columns.Companis).filter(columns.Companis.email == 'contact@techinnovators.com').first()
        if not existing_company:
            company = columns.Companis(
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
        existing_connect_company = db.query(columns.ConnectCompanis).filter(
            columns.ConnectCompanis.worker_id == user.id,
            columns.ConnectCompanis.company_id == company.id
        ).first()
        
        if not existing_connect_company:
            connect_company = columns.ConnectCompanis(
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