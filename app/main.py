
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)
        
app = FastAPI()
    
# ask chatgpt how to write good code to conect to db
while True: 
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', 
                                user='postgres', password='', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to DB")
        break
    except Exception as error:
        print("Conenct to DB Failed")
        print("Error: ", error)
        time.sleep(2)
    
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World"}