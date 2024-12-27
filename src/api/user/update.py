from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.user import UserResponse
from sqlalchemy.orm import Session  
from src.base.db import get_db
from src.other.utils import verify_password
from src.models.user import User
from sqlalchemy import select
from src.other.dependies import get_current_user

router = APIRouter()

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    old_password: str | None = None,
    new_password: str | None = None,
    db: Session = Depends(get_db),  
    current_user: dict = Depends(get_current_user),
):
    user = db.execute(select(User).where(User.id == current_user.get("user_id")))
    user = user.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    
    if old_password and new_password:
        if verify_password(old_password, user.hashed_password):
            user.hashed_password = new_password  
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect.",
            )

    db.commit()  
    db.refresh(user)  

    return user
