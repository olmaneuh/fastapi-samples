from db import Base
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class User(Base):
    __tablename__ = "users"

    id = Column(type_=Integer, primary_key=True, index=True)
    email = Column(type_=String, unique=True)
    username = Column(type_=String, unique=True)
    first_name = Column(type_=String)
    last_name = Column(type_=String)
    hashed_password = Column(type_=String)
    is_active = Column(type_=Boolean, default=True)
    role = Column(type_=String)


class UserCreateUpdateRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str


class UserPasswordUpdateRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=4)


class Token(BaseModel):
    access_token: str
    type: str


class Todo(Base):
    __tablename__ = "todos"

    id = Column(type_=Integer, primary_key=True, index=True)
    title = Column(type_=String)
    description = Column(type_=String)
    priority = Column(type_=Integer)
    complete = Column(type_=Boolean, default=False)
    owner_id = Column(ForeignKey("users.id"), type_=Integer)


class TodoCreateUpdateRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=3)
    complete: bool
