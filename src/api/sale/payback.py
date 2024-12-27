from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.base.db import get_db
from src.models import Sale, Product
from src.models.sale import StatusEnum
from src.other.dependies import require_role, get_current_user

router = APIRouter()


@router.post("/payback", dependencies=[Depends(require_role("manager"))])
def return_product(
    barcode: str,
    check_code: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    
    product_query = db.execute(select(Product).where(Product.barcode == barcode))
    product = product_query.scalars().first()

    
    sale_query = db.execute(
        select(Sale).where(
            Sale.product_id == product.id
            and Sale.seller_id == current_user.get("user_id")
            and Sale.random_numbers == check_code
        )
    )
    sale = sale_query.scalars().first()

    if sale:
        product.stock_quantity += sale.quantity_sold
        sale.status = StatusEnum.payback

        db.commit()
        db.refresh(sale)

    return sale
