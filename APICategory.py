from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
import metodAuth, columns, column_models
import models.category_models as category_models

router = APIRouter(
    prefix='/auth',
    tags=['category']
)

user_dependency = Annotated[dict, Depends(metodAuth.get_current_user)]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/category/add", status_code=status.HTTP_201_CREATED)
async def create_category(u: user_dependency, category: column_models.CategoryBaseCreateUpdate, db: db_dependency):    
    existing_category = db.query(columns.Category).filter(columns.Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail='Category already exists')  
    
    db_category = columns.Category(**category.model_dump())  
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return {"message": "Category created successfully", "category_id": db_category.id}


@router.get("/category/all", response_model=List[column_models.CategoryBase])
async def list_of_all_categories(u: user_dependency, db: db_dependency, skip: int = 0, limit: int = 100):
    # categories = db.query(columns.Category).offset(skip).limit(limit).all()  
    categories = (
        db.query(columns.Category)
        .order_by(columns.Category.id.desc())  # Change 'id' to the column you want to sort by
        .offset(skip)
        .limit(limit)
        .all()
    ) 
    return categories

@router.delete("/category/by-id/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category_by_id(u: user_dependency, category_id: int, db: db_dependency):
    sub_categories = db.query(columns.SubCategory).filter(columns.SubCategory.category_id == category_id).first()
    
    if sub_categories:
        raise HTTPException(status_code=404, detail='Category cannot be deleted because it has subcategories')

    category = db.query(columns.Category).filter(columns.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail='No category found with the given ID')

    db.delete(category)
    db.commit()

    return {"detail": "Category deleted successfully"}

@router.put("/category/{category_id}", status_code=status.HTTP_200_OK)
async def update_category(category_id: int, category: column_models.CategoryBaseCreateUpdate, u: user_dependency, db: db_dependency):
    
    existing_category = db.query(columns.Category).filter(columns.Category.id == category_id).first()
    
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
   
    if db.query(columns.Category).filter(columns.Category.name == category.name).first():
        raise HTTPException(status_code=400, detail="Category name already exists")
    
    existing_category.name = category.name
    db.commit()
    db.refresh(existing_category)

    return {"message": "Category updated successfully", "category_id": existing_category.id}


@router.post("/subcategory/add", status_code=status.HTTP_201_CREATED)
async def create_subcategory(u: user_dependency, sub_category: column_models.SubCategoryCreateBase, db: db_dependency):  
    existing_category = db.query(columns.Category).filter(columns.Category.id == sub_category.category_id).first()
    if not existing_category:
        raise HTTPException(status_code=400, detail='Category does not exist')
    
    existing_sub_category = db.query(columns.SubCategory).order_by(columns.SubCategory.id.desc()).filter(columns.SubCategory.name == sub_category.name).first()
    if existing_sub_category:
        raise HTTPException(status_code=400, detail='Subcategory already exists')
      
    db_sub_category = columns.SubCategory(**sub_category.model_dump())  
    db.add(db_sub_category)
    db.commit()
    db.refresh(db_sub_category)
    return {"message": "Subcategory created successfully", "subcategory_id": db_sub_category.id}

@router.get("/subcategory/all", response_model=List[column_models.SubCategoryBase])
async def list_of_all_subcategories(u: user_dependency, db: db_dependency, skip: int = 0, limit: int = 100):
    sub_categories = db.query(columns.SubCategory).order_by(columns.SubCategory.id.desc()).offset(skip).limit(limit).all()   
    return sub_categories

@router.get("/subcategories/by-category-id/{category_id}", status_code=status.HTTP_200_OK)
async def read_subcategory_by_category_id(u: user_dependency, category_id: int, db: db_dependency):  
    sub_categories = db.query(columns.SubCategory).order_by(columns.SubCategory.id.desc()).filter(columns.SubCategory.category_id == category_id).all()
    if not sub_categories:
        raise HTTPException(status_code=404, detail='No subcategories found for this category')
    return sub_categories

@router.delete("/subcategory/by-id/{subcategory_id}", status_code=status.HTTP_200_OK)
async def delete_subcategory_by_id(u: user_dependency, subcategory_id: int, db: db_dependency):
    sub_category = db.query(columns.SubCategory).filter(columns.SubCategory.id == subcategory_id).first()
    
    if not sub_category:
        raise HTTPException(status_code=404, detail='No subcategory found with the given ID')

    db.delete(sub_category)
    db.commit()  

    return {"detail": "Sub category deleted successfully"}

@router.put("/subcategory/{subcategory_id}", status_code=status.HTTP_200_OK)
async def update_subcategory(subcategory_id: int, sub_category: column_models.SubCategoryBaseUpdate, u: user_dependency, db: db_dependency): 
    existing_sub_category = category_models.update_subcategory(db, sub_category, subcategory_id)
    return {"message": "Subcategory updated successfully", "subcategory_id": existing_sub_category.id} 