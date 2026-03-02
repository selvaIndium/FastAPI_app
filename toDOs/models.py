from database import Base
from sqlalchemy import Column, Integer,String,Boolean


class Todos(Base):
    __tablename__ = "Todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    status = Column(Boolean)




