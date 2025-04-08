from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from typing import Optional
import columns, column_models
from auth import metod as mAuth
from typing import List
from datetime import datetime
from sqlalchemy.orm import joinedload
import models.category_models as category_models

router = APIRouter(
    prefix='/auth',
    tags=['product']
)

user_dependency = Annotated[dict, Depends(mAuth.get_current_user)]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/product/add", status_code=status.HTTP_201_CREATED)
async def create_product(u: user_dependency, product: column_models.ProductCreateBase, db: db_dependency): 
    
    db_product = columns.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    existing_sub_category = db.query(columns.SubCategory).filter(columns.SubCategory.id == product.sub_category_id).first()
    existing_sub_category.booked += product.count   

    existing_sub_category = category_models.update_subcategory(db, existing_sub_category, product.sub_category_id)

    return {"message": "Product created successfully", "product_id": db_product.id}

@router.get("/product/all", response_model=List[column_models.ProductBase])
async def list_of_all_products(u: user_dependency, db: db_dependency, skip: int = 0, limit: int = 100):
    products = (
        db.query(columns.Product)
        .outerjoin(columns.Category, columns.Product.category_id == columns.Category.id)
        .outerjoin(columns.SubCategory, columns.Product.sub_category_id == columns.SubCategory.id)
        .options(
            joinedload(columns.Product.category),
            joinedload(columns.Product.sub_category),
        )
        .order_by(columns.Product.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Convert ORM models to Pydantic response model
    product_list = [
        column_models.ProductBase(
            id=p.id,
            customer_name=p.customer_name,
            count=p.count,
            length=p.length,
            width=p.width,
            height=p.height,
            created_at=p.created_at,
            last_update=p.last_update,
            status=p.status,
            total_price=p.total_price,
            description=p.description,
            category_id=p.category_id,
            sub_category_id=p.sub_category_id,
            category_obj=column_models.CategoryBase(id=p.category.id, name=p.category.name) if p.category else None,
            sub_category_obj=column_models.SubCategoryBase(
                id=p.sub_category.id,
                name=p.sub_category.name,
                count = p.sub_category.count, 
                category_id=p.sub_category.category_id) if p.sub_category else None
        )
        for p in products
    ]

    return product_list

@router.put("/product/edit/{product_id}", status_code=status.HTTP_200_OK)
async def edit_connect_company(u: user_dependency, db: db_dependency, product_id: int, product: column_models.ProductBase):   
    product_model = db.query(columns.Product).filter(columns.Product.id == product_id).first()
    if not product_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )  
    
    
    if product.status == columns.StatusEnum.canceled:
        product.count = 0

    existing_sub_category = db.query(columns.SubCategory).filter(columns.SubCategory.id == product_model.sub_category_id).first()
    existing_sub_category.booked -= product_model.count-product.count     

    product_model.customer_name = product.customer_name
    product_model.length = product.length
    product_model.width = product.width
    product_model.height = product.height  
    product_model.count = product.count
    product_model.last_update = datetime.utcnow()
    product_model.status = product.status
    product_model.total_price=product.total_price
    product_model.description=product.description
    product_model.category_id = product.category_id
    product_model.sub_category_id = product.sub_category_id

    db.commit()
    existing_sub_category = category_models.update_subcategory(db, existing_sub_category, product_model.sub_category_id)

    return {"message": "Product updated successfully"}

@router.delete("/product/by-id/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product_by_id(u: user_dependency, product_id: int, db: db_dependency):
    product_model = db.query(columns.Product).filter(columns.Product.id == product_id).first()
    
    if not product_model:
        raise HTTPException(status_code=404, detail='No product found with the given ID')

    existing_sub_category = db.query(columns.SubCategory).filter(columns.SubCategory.id == product_model.sub_category_id).first()
    existing_sub_category.booked -= product_model.count      

    db.delete(product_model)
    db.commit() 

    existing_sub_category = category_models.update_subcategory(db, existing_sub_category, product_model.sub_category_id)

    return {"detail": "Product deleted successfully"}