from pydantic import BaseModel,Field
from fastapi import Body, FastAPI,Path
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
    Book(1, 'Computer Science Pro', 'codingwithselva', 'horrible', 0,2013),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5,2013),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5,2019),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2018),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2017),
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

@app.get("/books/filterBasedOnDate/{date}")
async def filter_based_on_date(date):
    nbooks = filter( lambda x: x.published_date == int(date),BOOKS)
    return list(nbooks)


#we are using Path coz, the {id} is passed as a path variable.
@app.delete("/books/deleteBook/{id}")
async def delete_book(id:int = Path(ge = BOOKS[0].id ,le=BOOKS[-1].id) if(BOOKS) 
                          else Path(ge = 0,le =0)) -> None:
    for b in BOOKS:
        if(b.id == id):
            BOOKS.remove(b)
            return
    
    raise IndexError("the id is out of bound.")

