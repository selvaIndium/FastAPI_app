from fastapi import FastAPI
import models
from database import engine
from crud import router as crud_router

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

app.include_router(crud_router)
