from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CreateBookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100, default=None)
    rating: int = Field(gt=-1, lt=6, default=0)
    published_date: int = Field(ge=1500, le=datetime.now().year)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "New book title",
                "author": " New book author full name",
                "description": "New book description",
                "rating": 5,
                "published_date": "Where was it published?",
            }
        }
    }


class UpdateBookRequest(BaseModel):
    id: int = Field(ge=0)
    title: str = Field(min_length=5)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(ge=1500, le=datetime.now().year)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "Book id to update",
                "title": "Updated book title",
                "author": " Updated book author full name",
                "description": "Updated book description",
                "rating": 5,
                "published_date": "Where was it published?",
            }
        }
    }
