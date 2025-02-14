from datetime import datetime
from fastapi import FastAPI, Path, Query, HTTPException
from models.book import Book
from schemas.book import CreateBookRequest, UpdateBookRequest
from starlette import status


app = FastAPI()


# to simulate the data in a database
BOOKS = [
    Book(0, "Study In Pink", "Arthur C. Doyle", "A Sherlock Holmes story", 5, 1700),
    Book(1, "Dune", "Frank Herbert", "A Dune story", 5, 1900),
    Book(2, "Outliers", "M. Gladwell", "An outlier", 1, 2024),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book(
    rating: int = Query(ge=0, le=5, default=None),
    published_date: int = Query(ge=1500, le=datetime.now().year, default=None),
):
    books = []
    for book in BOOKS:
        if not rating and not published_date:
            books.append(book)
            continue
        if rating and book.rating == rating:
            books.append(book)
            continue
        if published_date and book.published_date == published_date:
            books.append(book)
            continue
    return books


@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(id: int = Path(ge=0)):
    for book in BOOKS:
        if book.id == id:
            return book

    raise HTTPException(status_code=404, detail="Book not found.")


@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(request: CreateBookRequest):
    book = Book(**request.model_dump())
    book.id = generate_book_id()
    BOOKS.append(book)


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(request: UpdateBookRequest):
    if request.id < 0 or request.id >= len(BOOKS):
        raise HTTPException(status_code=404, detail="Book not found.")

    BOOKS[request.id] = request


@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int = Path(ge=0)):
    BOOKS.pop(id)


# utility functions
def generate_book_id():
    if not BOOKS:
        return 0
    return BOOKS[-1].id + 1  # get the last book id and increment by 1
