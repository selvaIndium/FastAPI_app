from fastapi import FastAPI
import models
from models import Todos
from sqlalchemy.orm import Session
from typing import Annotated
from database import engine,sessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

#gets u the db once. and then the session is cleaned up.
"""
The return version would break in FastAPI — the DB session closes before your route can query anything. yield is what keeps it alive until the route finishes.    
"""
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

dependency_db = Annotated[Session,get_db]

@app.get("/")
async def read_all(db:dependency_db):
    db = get_db()
    return db.query(Todos).all()

