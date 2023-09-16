
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# below is the allowed list of URLs that are allowed to communicate with the API

origins = ["*"]

# below is the security check that defines what and who and how is allowed to connect to our API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# models.Base.metadata.create_all(bind=engine)   not needed now that we have alembic

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") #without this decorator (which is signified by the @), the function does pretty much nothing, the decorator tells the function to use FastAPI
def root(): #@ = decorator, .get = http request method (get,post, put, delete), '/' = the path we use
    return {"message": "Welcome to my API bitches"}

#uvicorn main:app --reload
#BEFORE USING DATABASES THIS IS WHAT WE DID
# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
#             {"title": "favorite foods", "content": "I like pizza", "id": 2}]
# def find_index_post(id): #required to help us find posts to delete
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
# def find_post(id):
#     for p in my_posts:
#         if p['id'] ==id:
#             return p

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {'data': posts}

# CONSTRAINTS for tables
# PRIMARY ID, you choose a colum that is the deciding and primary identifier for a user, cant be changed, usually email but can be phone number, ssn, name would suck
# UNIQUES, adding a constraint to another colum similar to primary ID, that wasy you can have multiple things that arent allowd to be replicated
# NOT NULL, dissalowing any row to be left null, or have no response
# COMPOSITE ID; A PRIMARY KEY THAT SPANS MULTIPLE COLUMNS INSTEAD OF THE USUAL ONE, this is good so that we can control whether or not
# someone can like the same post or not. 


#SCHEMA MODELS/OYDANTIC MODEL
# Define the structure of an HTTP request and response
# Ensures that if someone wants to create data, POST, that it follows a set of rules defined
# Ensure that the response also follows the set rules
# SQL ALCHEMY MODEL
# Defines the columns of our "posts" tabel within postgres
# used to quesry created delete and upadte entries within our database


# CORS
# Cross Origin Resource Sharing
# allows you to make requests from a web browser on one domain to a server on a adifferent domain
# by default, our API will only alow web browsers running on the same domain as our server to make requests to it
# you can only access API's from the same domain
# so you cant access google.com API from ebay