from .auth import get_current_user
from db import engine, SessionMaker
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todo, TodoCreateUpdateRequest
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated


router = APIRouter()


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
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    return db.query(Todo).filter(Todo.owner_id == user.get("id")).all()


@router.get("/todo/{id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependecy, db: db_dependency, id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    todo = (
        db.query(Todo)
        .filter(Todo.id == id)
        .filter(Todo.owner_id == user.get("id"))
        .first()
    )

    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {id} not found.")

    return todo


@router.post("/todo/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependecy, db: db_dependency, request: TodoCreateUpdateRequest
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    todo = Todo(**request.model_dump(), owner_id=user.get("id"))

    db.add(todo)
    db.commit()


@router.put("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependecy,
    db: db_dependency,
    request: TodoCreateUpdateRequest,
    id: int = Path(gt=0),
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    todo = (
        db.query(Todo)
        .filter(Todo.id == id)
        .filter(Todo.owner_id == user.get("id"))
        .first()
    )

    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {id} not found.")

    todo.title = request.title
    todo.description = request.description
    todo.priority = request.priority
    todo.complete = request.complete

    db.add(todo)
    db.commit()


@router.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependecy, db: db_dependency, id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed.")

    todo = (
        db.query(Todo)
        .filter(Todo.id == id)
        .filter(Todo.owner_id == user.get("id"))
        .first()
    )

    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {id} not found.")

    db.query(Todo).filter(Todo.id == id).filter(Todo.owner_id == user.get("id")).delete()

    db.commit()
