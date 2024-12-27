from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as http_err:
            raise http_err
        except SQLAlchemyError as db_err:
            db = kwargs.get("db")
            if db:
                db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(db_err)}",
            )
        except Exception as err:
            db = kwargs.get("db")
            if db:
                db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(err)}",
            )

    return wrapper
