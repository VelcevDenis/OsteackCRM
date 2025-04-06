from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import  HTTPException
from sqlalchemy.orm import Session
import columns, column_models

def update_subcategory(db: Session, sub_category: column_models.SubCategoryBaseUpdate, subcategory_id: int):
    existing_sub_category = db.query(columns.SubCategory).filter(columns.SubCategory.id == subcategory_id).first()
    
    if not existing_sub_category:
        raise HTTPException(status_code=404, detail="Subcategory not found")    
    
    existing_sub_category.name = sub_category.name
    existing_sub_category.count =sub_category.count
    existing_sub_category.booked = (
        existing_sub_category.booked if sub_category.booked == -1 else sub_category.booked
    )
    existing_sub_category.height = sub_category.height
    existing_sub_category.width = sub_category.width
    existing_sub_category.length = sub_category.length
    existing_sub_category.price_per_piece = sub_category.price_per_piece
    db.commit()
    db.refresh(existing_sub_category)

    return existing_sub_category