from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.base.db import get_db
from src.models import Product, Sale
from src.other.dependies import require_role, get_current_user
from src.other.errorrs import handle_exceptions
from src.models.sale import StatusEnum

router = APIRouter()


@router.post("/", dependencies=[Depends(require_role("seller"))])
@handle_exceptions
def create_sale(
    barcode: str,
    quantity_sold: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    
    product_query = db.execute(select(Product).where(Product.barcode == barcode))
    product = product_query.scalars().first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product with the given barcode not found.",
        )

    
    if quantity_sold > product.stock_quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock available.",
        )

    
    sale_query = db.execute(
        select(Sale).where(
            Sale.product_id == product.id,
            Sale.seller_id == current_user.get("user_id"),
            Sale.status == StatusEnum.selling,
        )
    )
    sale = sale_query.scalars().first()

    
    product.stock_quantity -= quantity_sold

    if sale:
        sale.quantity_sold += quantity_sold
        db.commit()
        db.refresh(sale)
        return sale
    else:
        
        new_sale = Sale(
            product_id=product.id,
            seller_id=current_user.get("user_id"),
            quantity_sold=quantity_sold,
            status=StatusEnum.selling,
        )
        db.add(new_sale)

        db.commit()
        db.refresh(new_sale)
        return new_sale
