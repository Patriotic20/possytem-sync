from fastapi import APIRouter, Depends
from src.schemas.product import ProductResponse, ProductCreate
from sqlalchemy.orm import Session
from src.base.db import get_db
from sqlalchemy import select
from src.models.product import Product

router = APIRouter()

# dependencies=[Depends(require_role("Admin"))]

@router.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    action = db.execute(select(Product).where(Product.barcode == product.barcode)).scalars().first()

    if action:
        action.stock_quantity += 1
        db.commit()
        return action
    else:
        new_product = Product(**product.model_dump())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
