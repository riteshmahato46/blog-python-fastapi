from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post_router, user_router, auth_router

models.Base.metadata.create_all(bind=engine)
        
app = FastAPI()

app.include_router(post_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)