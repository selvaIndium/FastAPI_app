from pydantic import BaseModel
from fastapi import Body, FastAPI

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithselva', 'horrible', 0, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

@app.get("/books/getBooks")
def get_books():
    return BOOKS

@app.post("/books/sendBooks")
def send_books(bookreq : BookRequest):
    BOOKS.append(**bookreq.dict())
    
