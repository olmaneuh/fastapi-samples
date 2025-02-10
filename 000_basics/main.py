from fastapi import Body, FastAPI


app = FastAPI()


# to simulate the data in a database
BOOKS = [
    {"id": 0, "title": "Sapiens", "author": "Yuval Harari", "category": "History"},
    {"id": 1, "title": "Dune", "author": "Frank Herbert", "category": "Sci-Fi"},
    {"id": 2, "title": "Becoming", "author": "M. Obama", "category": "Memoir"},
    {"id": 3, "title": "Room", "author": "Emma Donoghue", "category": "Fiction"},
    {"id": 4, "title": "Verity", "author": "C. Hoover", "category": "Thriller"},
    {"id": 5, "title": "Circe", "author": "M. Miller", "category": "Fantasy"},
    {"id": 6, "title": "Outliers", "author": "M. Gladwell", "category": "Self-Help"},
    {"id": 7, "title": "Normal People", "author": "S. Rooney", "category": "Romance"},
    {"id": 8, "title": "The Road", "author": "C. McCarthy", "category": "Dystopian"},
    {"id": 9, "title": "It Ends Us", "author": "C. Hoover", "category": "Drama"},
]


# simple path
@app.get("/books")
async def get_all_books():
    return BOOKS


# path parameters
@app.get("/books/{book_id}")
async def get_book_by_id(id: int):
    for book in BOOKS:
        if book.get("id") == id:
            return book


# query parameters
@app.get("/books/")
async def get_books_by_author(author: str):
    books_by_author = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_by_author.append(book)
    return books_by_author


# combining path parameters and query parameters
@app.get("/books/{category}/")
async def get_books_by_category_author(category: str, author: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("category").casefold() == category.casefold()
            and book.get("author").casefold() == author.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


# post request
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


# put request
@app.put("/books/update_book/{book_id}")
async def update_book(id: int, updated_book=Body()):
    BOOKS[id] = updated_book


# delete request
@app.delete("/books/delete_book/{book_id}")
async def delete_book(id: int):
    BOOKS.pop(id)
