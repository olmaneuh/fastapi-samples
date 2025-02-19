from .auth import get_current_user
from db import engine, SessionMaker
from fastapi import APIRouter, Depends, HTTPException, Path
from models import User, UserPasswordUpdateRequest
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated


router = APIRouter(prefix="/user", tags=["user"])


# provides a new SQLAlchemy session
def get_db():
    db = SessionMaker()  # create a new database session
    try:
        yield db  # provide it to the request handler
    finally:
        db.close()  # close the session after request is done


db_dependency = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependecy, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    return db.query(User).filter(User.id == user.get("id")).first()


@router.put("/update_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    user: user_dependecy, db: db_dependency, request: UserPasswordUpdateRequest
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    current_user = db.query(User).filter(User.id == user.get("id")).first()

    if not bcrypt_context.verify(
        request.current_password, current_user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="The current password not match.")

    current_user.hashed_password = bcrypt_context.hash(request.new_password)

    db.add(current_user)
    db.commit()
