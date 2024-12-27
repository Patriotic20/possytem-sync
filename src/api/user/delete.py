from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.base.db import get_db
from src.models.user import User
from sqlalchemy import select
import uuid

router = APIRouter()


@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User successfully deleted"}
