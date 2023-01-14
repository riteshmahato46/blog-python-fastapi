# Python REST API (FastAPI)
Barebones python(3.7) Web service demonstrating how to create REST APIs using FastAPI framework.

### Features
- User login (Authenticate using JWT)
  - Password hashing using [passlib](https://pypi.org/project/passlib/) library and [bcrypt](https://pypi.org/project/bcrypt/) algorithm 
  - JWT Token library - [python-jose](https://github.com/mpdavis/python-jose) with cryptographic backend [pyca/cryptography](https://cryptography.io/en/latest/)
  
- REST API 
  - Framework used - [FastAPI](https://fastapi.tiangolo.com/)
  - Create/Read/Update/Delete API for Posts (CRUD).
  - Pagination support in GET all posts API using `limit` and `offset` from sqlalchemy ORM features\
  `http://127.0.0.1:8000/posts?limit=5&skip=5`
  - Search support for post title using query params\
  `http://127.0.0.1:8000/posts?search=yo`
  - Users can *Like*/*Upvote* posts. Check Swagger doc `http://127.0.0.1:8000/docs` for API.\
  In the payload JSON `direction` of `1` is *like* and `0` is *unlike*.
  - Request/Response model validation using [pydantic](https://docs.pydantic.dev/)

- Database - Postgres
  - ORM - [SQLAlchemy](https://www.sqlalchemy.org/), DB driver - [Psycopg2](https://pypi.org/project/psycopg2/)
  - DB Table Migration/update implemented using [alembic](https://alembic.sqlalchemy.org/en/latest/). 
  - DB schemas inside [persistence/db_models.py](https://github.com/riteshmahato46/blog-python-FastAPI/blob/master/app/persistence/db_models.py).

- Configs (Urls, secrets, db connection strings, environment vars)
  - All configs are stored in [.env](https://github.com/riteshmahato46/blog-python-fastapi/blob/master/.env) file and read in code using [python-dotenv](https://pypi.org/project/python-dotenv/) pydantic models. In production this file should not be checked in to git to keep passwords and secrets safe

-------------------------------------------------------------

### How to run

- Clone the repository
- Install all requirements (create a venv in you want to contain the installations)\
`pip install -r requirements.txt`
- Start Postgres Server on you local system
  - Create a database named **fastapi** and owner named **postgres** OR change settings [here](https://github.com/riteshmahato46/blog-python-FastAPI/blob/594656b2358db4d446968f135ecdaac69ee2b87c/app/persistence/database.py#L5) as per your db/owner names
- Run the web server locally using uvicorn \
`python -m uvicorn app.main:app --reload`
- Navigate to `http://127.0.0.1:8000/docs` on your browser to get swagger docs for all APIs and their payloads.
- The flow is to first create a new user using the *Create User API* and then Login using the *Login API*. This will give you the access token. Execute all other APIs by providing the bearer access token as the header.
