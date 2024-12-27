from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from src.base.db import get_db
from src.models import Sale
from datetime import date

router = APIRouter()


@router.get("/")
def get_monthly(
    start: date | None = None,
    end: date | None = None,
    db: Session = Depends(get_db),
):
    query = select(Sale).options(
        joinedload(Sale.product), 
        joinedload(Sale.seller),  
    )

    if start:
        query = query.where(Sale.sale_date >= start)
    if end:
        query = query.where(Sale.sale_date <= end)

    month = db.execute(query)
    result = month.scalars().all()

    sales_data = []

    for sale in result:
        sales_data.append(
            {
                "id": sale.id,
                "product_name": sale.product.name,
                "seller_name": sale.seller.username,
                "quantity_sold": sale.quantity_sold,
                "sale_date": sale.sale_date,
                "payment_method": sale.payment_method,
                "discount": sale.discount,
                "tax": sale.tax,
                "status": sale.status.value,
                "random_numbers": sale.random_numbers,
            }
        )
    return sales_data
