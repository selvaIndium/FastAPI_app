from fastapi import Body,Depends,HTTPException,status, APIRouter
from models import Todos
from sqlalchemy.orm import Session
from typing import Annotated
from database import sessionLocal
from pydantic import BaseModel,Field

router = APIRouter()

#gets u the db once. and then the session is cleaned up.
"""
The return version would break in FastAPI — the DB session closes before your route can query anything.
yield is what keeps it alive until the route finishes.    
"""
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

dependency_db = Annotated[Session,Depends(get_db)]

#passing basemodel as a param is the only time there is actual validation.
class toDoRequest(BaseModel):
    title : str = Field(min_length=1)
    description :str = Field(min_length=1)
    priority : int = Field(le = 5, ge= 1)
    status : bool

@router.get("/")
async def read_all(db:dependency_db):
    return db.query(Todos).all()

@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(db:dependency_db, todo_id:int):
    todo_by_id = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_by_id:
        return todo_by_id
    else:
        raise HTTPException(status_code=404, detail="")

@router.post("/todo/post_todo",status_code=status.HTTP_201_CREATED)
async def post_todo(db:dependency_db,n_todo:toDoRequest = Body(...)):
    #todos 
    todo = Todos(**n_todo.model_dump())
    db.add(todo)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["spme"])
async def update_todo(db:dependency_db, todo_id:int, todo: toDoRequest):
    """When you query an object, it's already attached to the session. Adding it again won't break anything, but it's redundant."""
    #this fixes all confusion about adding things.
    upd_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    
    #rubbish.
    # attributes = filter(lambda x: x != "_sa_instance_state",upd_todo.__dict__.keys())
    
    # for attr in attributes:
    #     upd_todo[attr] = todo[attr]
    
    # db.add(upd_todo)  
    # db.commit()

    if(not upd_todo):
        raise HTTPException(status_code=404, detail="not found")
    
    #if the user passed only title, rest of them get wiped, so we need to find another routerroach.
    upd_todo.title = todo.title
    upd_todo.description = todo.description
    upd_todo.status = todo.status
    upd_todo.priority = todo.priority

    db.commit()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def todo_delete(db:dependency_db,todo_id:int):
    del_todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if(not del_todo):
        raise HTTPException(status_code=404, details ="no todo on the id")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
