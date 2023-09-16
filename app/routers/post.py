from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", #this makes it so we dont have to type the same path every request, now its just a / unless specified otherwise
    tags= ['Posts']
)

@router.get('/', response_model=List[schemas.PostOUT]) #List import needed for getting multiple posts, otherwise it wont print list
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""): #the limit is how many posts someone can get if they search all with no limit, we capped it at 10
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute('''SELECT * FROM posts''') THIS IS USING RAW SQL, DOING QUERIES WITH DB IS USING THE ORM
    # posts = cursor.fetchall
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, 
                        models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
                        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)): #this part at the end is what asks users to verify token to be able to post
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() #NEEDED FOR CHANGES TO BE FINALIZED IN SQL
    # print(post) #if we wanted just part of the data we could go post.content or post.title
    # print(post.dict()) #used to convert pydantic model to dictionary
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000000) #creates a random ID for each post
    # my_posts.append(post.dict()) # adds to myposts which is our post history
    new_post = models.Post(owner_id=current_user.id, **post.dict()) #this makes its so we dont have to write out what each post requires each time, it just makes a dictionary of what the requirements are from the Post Class and does it for us
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post # .dict() turns it into a dictionary,so we can have it send back the entire post data instead of just "post" for confirmation

#CRUD
# CREATE = POST         /posts                @app.post("/posts")
# 
# READ =   GET          /posts/:id            @app.get("/posts/{id}")
#      =   GET          /posts                @app.get("/posts")
# 
# UPDATE = PUT/PATCH    /posts/:id            @app.put("/posts/{id}")
#          put you change everything, patch just the one field
# DELETE = DELETE       /posts/:id            @app.delete("/posts/{id}")

@router.get("/{id}", response_model=schemas.PostOUT)
def get_post(id: int, db: Session = Depends(get_db)): #the :int part makes it so it is required for the front end to enter an integer for it to even work and will give them a valid
# error message for what they did wrong. otherwise it just says "INTERNAL SYSTEM ERROR". The response is for sending 404 or other server messages to let front end know if an unkown id is entered
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()#do .first when you know only one thing is being searched for
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, 
                        models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id
                        ).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with ID: {id} was not found. ')
    return post

# if you do type(thing you put here) you can see the type of thing it is; str, bool, float, int
# order of functions matter more when working with API. if I had a fucntion that gathered latest posts AFTER my id function,
#      an error would be thrown because the id function requires integers, nad python would look at that first. "latest" isnt one, so latest would have to go before the id function


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None: #we need this if soeone tries to delete a post that doestn exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'post with id: {id} does not exist')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Not authorized to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) #you dont type your own message here becasue you dont want to send data back when you delete something


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                (post.title, post.content, post.published, (str(id),)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None: #we need this if soeone tries to delete a post that doestn exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'post with id: {id} does not exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Not authorized to perform requested action')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()