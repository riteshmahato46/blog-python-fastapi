# Python REST API (FastAPI)
Barebones python(3.7) Web service demonstrating how to create REST APIs using FastAPI framework.

### Features
- User login (Authenticate using JWT)
- Create/Read/Update/Delete Posts (CRUD)
- Store data in Postgres Database

### Frameworks used
#### FastAPI 
GET, POST, PUT, DELETE API examples using @app and @router

#### Pydantic
Models for Request/Response and pydantic auto validation in REST APIs

#### Postgres
ORM used - **SQLAlchemy**\
DB driver - **Psycopg2**

#### Authentication
User password hash - **bcrypt** hashing using **passlib** library\
JWT Token  library - [python-jose](https://github.com/mpdavis/python-jose) with cryptographic backend [pyca/cryptography](https://cryptography.io/en/latest/)

-------------------------------------------------------------

**Python libraries used (pip freeze)**
- anyio==3.6.2
- bcrypt==4.0.1
- cffi==1.15.1
- click==8.1.3
- cryptography==39.0.0
- dnspython==2.2.1
- ecdsa==0.18.0
- email-validator==1.3.0
- fastapi==0.89.0
- greenlet==2.0.1
- h11==0.14.0
- idna==3.4
- passlib==1.7.4
- psycopg2==2.9.5
- pyasn1==0.4.8
- pycparser==2.21
- pydantic==1.10.4
- python-jose==3.3.0
- rsa==4.9
- six==1.16.0
- sniffio==1.3.0
- SQLAlchemy==1.4.46
- starlette==0.22.0
- typing_extensions==4.4.0
- uvicorn==0.20.0