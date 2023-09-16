from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


# class Post(BaseModel): #this moderates what is able to be sent back to the API
#     title: str
#     content: str
#     published: bool = True #putting the true here before runnin it makes true the default value


# CREATING MULTIPLE CLASSES ALLOWS YOU TO HAVE MULTIPLE MODELS FOR THE SPECIFIC THING YOU ARE REFERENCING
# THE POSTBASE IS THE BASE MODEL< YOU CAN ADD OTHERS THAT FOLLOW ITS RULES OR ONLY SOME< OR MORE
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
   pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config: 
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostResponse(PostBase): #we put this class in our POST function and this is all the info that will return to user when they create
    id: int
    created_at: datetime #the other trhee, title content and published are inherited
    owner_id: int #this shows who posted the post, putting it here and not in the basemodelmakes it so that the creator doesnt need to 
    #figure out their id to make a post, and our logic will fill in the blanks for them when they create a post
    owner: UserOut #this is the owner schema that will return on posts instead of just their id
    class Config: #If we dont have this in our class, we will get an error becasue the pydanctic model looks for dicts, this converts the sqlalchemy model to a pydantic model first
        orm_mode = True

class PostOUT(BaseModel):
    Post: PostResponse
    votes: int

    class Config: 
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #determines how much a lieks can go up or down per vote, this can go negative however, but its fine for this, dude wasnt sure how to only specify 0 or 1
