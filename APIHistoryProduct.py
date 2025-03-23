# from typing import Annotated
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from starlette import status
# from database import SessionLocal
# from typing import Optional
# import metodAuth, columns, column_models
# from typing import List
# # import logging
# # logger = logging.getLogger("uvicorn")

# router = APIRouter(
#     prefix='/auth',
#     tags=['historyProduct']
# )

# user_dependency = Annotated[dict, Depends(metodAuth.get_current_user)]

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()    

# db_dependency = Annotated[Session, Depends(get_db)]


# @router.post("/historyProduct/add", status_code=status.HTTP_201_CREATED)
# async def create_product(u: user_dependency, historyProduct: column_models.HistoryProductBase, db: db_dependency):    
#     db_historyProduct = columns.Companis(**historyProduct.dict())
#     db.add(db_historyProduct)
#     db.commit()
#     db.refresh(db_historyProduct)
#     return {"message": "History Product created successfully", "historyProduct_id": db_historyProduct.id}

# @router.get("/historyProduct/all", response_model=List[column_models.HistoryProductBase])
# async def list_of_all_history_products(u: user_dependency, db: db_dependency, skip:int=0, limit:int=100):
#     historyProducts = db.query(columns.HistoryProduct).offset(skip).limit(limit).all()
#     return historyProducts

# @router.put("/historyProduct/edit/{history_prod_id}", status_code=status.HTTP_200_OK)
# async def edit_history_product(u: user_dependency, db: db_dependency, history_prod_id: int, historyProduct: column_models.EditHistoryProductBase):   
#     history_prod_model = db.query(columns.HistoryProduct).filter(columns.HistoryProduct.id == history_prod_id).first()
#     if not history_prod_model:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Connect company with id {history_prod_id} not found"
#         )   
 
#     history_prod_model.is_approved = 0 if historyProduct.status == columns.StatusEnum.pending else history_prod_model.is_approved   

#     db.commit()

#     return {"message": "History product status updated successfully"}


