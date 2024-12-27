from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.base.db import get_db
from src.models.product import Product

# response_model=ProductResponse
router = APIRouter()

@router.put("/products/{product_id}")
def update_product(
    barcode: str,
    name: str | None = None,
    stock_quantity: int | None = None,
    price: float | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
):
    product = db.execute(select(Product).where(Product.barcode == barcode)).scalars().first()

    if not product:
        return {"error": "Product not found"}

    if name:
        product.name = name
    if stock_quantity:
        product.stock_quantity = stock_quantity
    if price:
        product.price = price
    if category:
        product.category = category

    db.commit()
    db.refresh(product)
    return product
