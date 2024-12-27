from functools import wraps

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError, DBAPIError

from src.other.utils import oauth2_scheme, decode_token
from sqlalchemy import select
from src.models import User
from sqlalchemy.orm import Session  
from src.base.db import get_db


def get_current_user(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)  
):
    payload = decode_token(token)
    username: str = payload.get("sub")
    email: str = payload.get("email")
    role: str = payload.get("role")
    user_id: str = payload.get("user_id")

    user = db.execute(select(User).where(User.id == user_id))
    user = user.scalars().first()

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User invalid authentication",
        )
    return {"username": username, "role": role, "user_id": user_id, "email": email}


def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: Requires {required_role} role",
            )
        return user

    return role_checker


def db_rollback(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = kwargs.get('db', Depends(get_db))
        try:
            result = func(*args, **kwargs)
            db.commit()  
        except (IntegrityError, DBAPIError) as e:
            db.rollback()  
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while updating",
            )

        return result

    return wrapper
