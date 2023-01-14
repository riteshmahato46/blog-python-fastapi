from fastapi import FastAPI
from .persistence import db_models
from .persistence.database import engine
from .routers import post_router, user_router, auth_router, like_router

# This will create all tables in 'fastapi' postgres db at startup
# Running first version of alembic will do the same 
db_models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# URL Routers/ Controllers registration
app.include_router(post_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(like_router.router)