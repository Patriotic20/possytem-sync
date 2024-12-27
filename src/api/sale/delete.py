from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.base.db import get_db
from sqlalchemy import select
from src.models.sale import Sale


router = APIRouter()


@router.delete("/")
def delete_sale(db: Session = Depends(get_db)):
    sale = db.execute(select(Sale))
    sale = sale.scalars().all()

    for sale_item in sale:
        db.delete(sale_item)
    db.commit()
    return "Delete"
