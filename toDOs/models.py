from database import Base
from sqlalchemy import Column, Integer,String,Boolean,ForeignKey

class users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email_id = Column(String,unique=True)
    user_name = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_pwd = Column(String,unique= True)
    is_active = Column(Boolean)
    role = Column(String)

class Todos(Base):
    __tablename__ = "Todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    status = Column(Boolean)

    #foreignkey
    user_id = Column(Integer, ForeignKey(users.user_id))