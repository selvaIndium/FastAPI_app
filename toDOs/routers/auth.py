from datetime import datetime, timedelta, timezone

from fastapi import APIRouter,Depends,HTTPException
from database import engine
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
from database import sessionLocal
from models import users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
import yaml
from jose import jwt

with open("../secrets.yaml", 'r') as file:
    secrets = yaml.safe_load(file)

SECRET_KEY = secrets["SECRET_KEY"]

router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

class TOKEN(BaseModel):
    access_token:str
    token_type:str

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
def get_all_users(db:dependency_db, offset:int =0, limit:int=100):
    usr_db = db.query(users).offset(offset).limit(limit)
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

    db.add(new_user)
    db.commit()

def authenticate_user(username:str, pwd:str, db):
    user = db.query(users).filter(users.user_name == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(pwd, user.hashed_pwd):
        return False
    return user

def create_token(username:str, user_id:int, time:timedelta):
    encode = {'sub':username, 'id':user_id}
    expires = datetime.now(timezone.utc) + time
    encode.update({'exp' : expires})

    return jwt.encode(encode, SECRET_KEY,algorithm=secrets["algorithm"])


@router.post("/access_token/",response_model=TOKEN)
def get_access_token(db:dependency_db, form_data : form_format):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user.user_name, user.user_id, timedelta(minutes=20))
    return {'access_token': token, 'token_type' : 'bearer'}
