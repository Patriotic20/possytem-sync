from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  
from sqlalchemy import select
from src.base.db import get_db
from src.models.user import User

router = APIRouter()

@router.get("/")
def list_users(
    last_name: str | None = None,
    first_name: str | None = None,
    db: Session = Depends(get_db),  
):
    if not last_name and not first_name:
        users = db.execute(select(User))
        users = users.scalars().all()
        return users
    if last_name and first_name:
        user = db.execute(
            select(User).where(
                User.first_name == first_name and User.last_name == last_name
            )
        )
        user = user.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
