from fastapi import FastAPI
from .persistence import models
from .persistence.database import engine
from .routers import post_router, user_router, auth_router
from .config import settings

models.Base.metadata.create_all(bind=engine)
        
app = FastAPI()

app.include_router(post_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)