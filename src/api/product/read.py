from fastapi import APIRouter, Depends
from typing import List
from src.schemas.product import ProductResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.base.db import get_db
from src.models.product import Product

router = APIRouter()

@router.get("/products", response_model=List[ProductResponse])
def list_products(barcode: str, db: Session = Depends(get_db)):
    product = db.execute(select(Product).where(Product.barcode == barcode)).scalars().first()
    return product

