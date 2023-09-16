from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
#This is using an ORM, which is a way to talk to SQL and use SQL qithout actually going into the raw version of it, 
# and only sticking to puthon code, everything you see here is the same as what we did to make the posts table in SQL

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = 'CASCADE'), nullable=False)

    owner = relationship("User") #lets say you want the persons name or username
    #published and not their ID when they post, this is all you do, create a relationship with the User class/table

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable = False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))

class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key = True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key = True)