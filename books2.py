from pydantic import BaseModel,Field
from fastapi import Body, FastAPI
from typing import Optional
import datetime

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    # published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int]= Field(description="id is optional.", default=None)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1)
    rating: int = Field(gt = 1, lt = 5)
    published_date: int = Field(ge=1900, le=datetime.date.today().year)

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithselva', 'horrible', 0, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

@app.get("/books/getBooks")
async def get_books():
    return BOOKS


def find_bookId(book:BookRequest) -> BookRequest:
    if(not len(BOOKS)):
        book.id = 1
    else:
        book.id = BOOKS[-1].id +1
    return book

@app.post("/books/sendBooks")
async def send_books(bookreq : BookRequest):
    nbook = Book(**bookreq.model_dump())
    nbook =find_bookId(nbook)
    BOOKS.append(nbook)

