from fastapi import FastAPI, Depends
from typing import Annotated
import columns
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import APIAuth, APIUser, APIRole, APICompany, APIConnectCompany, APIProduct, APICategory, APIHistoryProduct
import metodAuth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(APIAuth.router)
app.include_router(APIUser.router)

app.include_router(APIRole.router)
app.include_router(APICompany.router)
app.include_router(APIConnectCompany.router)

app.include_router(APICategory.router)

app.include_router(APIProduct.router)
# app.include_router(APIHistoryProduct.router)

columns.Base.metadata.create_all(bind=engine)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(metodAuth.get_current_user)]

#REGION controller methods









