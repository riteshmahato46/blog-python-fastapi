from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.persistence import db_models
from app.persistence.database import engine
from app.routers import post_router, user_router, auth_router, like_router

# This will create all tables in 'fastapi' postgres db at startup
# Running first version of alembic will do the same 
db_models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL Routers/ Controllers registration
app.include_router(post_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(like_router.router)

@app.get("/")
async def main():
    return {"Ping": "Ok"}