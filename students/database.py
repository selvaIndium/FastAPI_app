
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQL_ALCHEMY_URL  = "sqlite:///./students.db"

#setting check same thread to false, to enable concurrency.
engine = create_engine(url=SQL_ALCHEMY_URL, connect_args={'check_same_thread' : False})

#flush is like comit, u can rollback. draft save.
#comit is like push, u push it its done
sessionLocal = sessionmaker(autocommit=False,autoflush= False, bind=engine)

Base = declarative_base()
