from fastapi import APIRouter,Depends
from database import engine
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
from database import sessionLocal
from models import users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

dependency_db = Annotated[Session,Depends(get_db)]
form_format = Annotated[OAuth2PasswordRequestForm, Depends()]

class create_user_request(BaseModel):
    email_id : str
    user_name : str
    first_name : str
    last_name : str
    pwd : str
    role : str

@router.get("/user/")
def get_all_users(db:dependency_db):
    usr_db = db.query(users).all()
    return usr_db

@router.post("/user/")
def post_user(db:dependency_db, user_req:create_user_request):
    new_user = users()

    new_user.email_id = user_req.email_id
    new_user.user_name = user_req.user_name
    new_user.first_name = user_req.first_name
    new_user.last_name = user_req.last_name
    new_user.hashed_pwd = bcrypt_context.hash(user_req.pwd)
    new_user.role = user_req.role

    db.add()
    db.commit()

@router.post("/access_token/")
def get_access_token(db:dependency_db, form_data : form_format):
    