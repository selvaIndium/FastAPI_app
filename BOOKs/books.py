from fastapi import FastAPI,Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

#the async is optional fastapi knows if its async or not and does it implicitly.
@app.get("/")
async def first_api():
    return {"message" : "hi selva!"}

@app.get("/books")
def getBooks():
    return BOOKS

@app.get("/book/hello")
def sayHello():
    return "hi hello!"

#dynamic params

#query params
@app.get("/books/{book_title}")
def get_books_by_title_category(book_title:str, category:str|None = None)->dict:
    if(category):
        filtered_books = filter(lambda x: x["title"].casefold() == book_title.casefold() 
                                        and x["category"] == category, BOOKS)
        return list(filtered_books)[0]
    else:
         #overcomplicated for fun lmao.
        filtered_books = map( lambda x : x if (x["title"].casefold() == book_title.casefold()) 
                                            else " ",BOOKS)
        filtered_book_v2 = filter(lambda x : x != " ",filtered_books)
        return list(filtered_book_v2)[0]

#add book
@app.post("/books/postBooks")
def postBook(nbook = Body()):
    BOOKS.append(nbook)

#update book
@app.put("/books/updatebook")
def update_bookTitle(nbook = Body()) -> None:
    for i in range(len(BOOKS)):
        if(BOOKS[i]["title"] == nbook["title"]):
            BOOKS[i] = nbook
            break

#delete book based on category
@app.delete("/books/deleteBook/{book_category}")
def delete_book_byCategory(book_title):
    books_toBe_deleted = filter(lambda x: x["title"] == book_title, BOOKS)
    for i in books_toBe_deleted:
        BOOKS.remove(i)
            

    
    