from fastapi import APIRouter,Depends,status
from models import student
from database import Base,sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter()

class students(BaseModel):
    name : str
    marks: int

def get_db():
    db = sessionLocal()
    try:
        yield db
    except:
        return db.close()

dependency_db = Annotated[Session, Depends()]
    
@router.get("/get_students/")
def get_all(db:dependency_db):
    return db.query(student).all()

@router.post("/post_students/", status_code=status.HTTP_201_CREATED)
def post_student(db:dependency_db, std: students):
    nstud = student(**nstud)
    db.add(nstud)
    db.commit()

@router.put("/update_stud/{id}", status_code=status.htt)
def update_student(db:dependency_db,id:int, std: students):
    filtered_db = db.query(student).filter(student.id == id).first()
    filtered_db.name = std.name
    filtered_db.marks = std.marks

    db.commit()

@router.delete("/delete_student/{id}")
def del_student(db:dependency_db, id:int):
    db_mod = db.query(student).filter(student.id == id)
    db.delete(db_mod)
    db.commit()