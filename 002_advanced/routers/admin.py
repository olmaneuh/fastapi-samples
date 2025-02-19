from .auth import get_current_user
from db import engine, SessionMaker
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todo, TodoCreateUpdateRequest
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated


router = APIRouter(prefix="/admin", tags=["admin"])


# provides a new SQLAlchemy session
def get_db():
    db = SessionMaker()  # create a new database session
    try:
        yield db  # provide it to the request handler
    finally:
        db.close()  # close the session after request is done


db_dependency = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_dependecy, db: db_dependency):
    if not user or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    return db.query(Todo).all()


@router.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependecy, db: db_dependency, id: int = Path(gt=0)):
    if not user or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    todo = db.query(Todo).filter(Todo.id == id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.query(Todo).filter(Todo.id == id).delete()

    db.commit()
