from database import Base
from sqlalchemy import Column, Integer, String

class student(Base):

    __tablename__  = "students"

    id = Column(Integer, primary_key= True, index= True)
    name = Column(String)
    marks = Column(Integer)
