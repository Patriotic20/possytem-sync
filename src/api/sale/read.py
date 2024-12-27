from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.base.db import get_db
from src.models import Sale, Product
from src.other.errorrs import handle_exceptions
from src.other.dependies import require_role

router = APIRouter()


@handle_exceptions
@router.get("/read", dependencies=[Depends(require_role("Seller"))])
def read_sale(db: Session = Depends(get_db)):
    try:
        
        query = select(Sale).join(Product)
        result = db.execute(query)
        sales = result.scalars().all()

        if not sales:
            raise HTTPException(
                status_code=404, detail="No sales found for the given barcode"
            )

        return sales

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
