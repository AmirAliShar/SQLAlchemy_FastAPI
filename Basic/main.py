from fastapi import FastAPI, Depends,status,HTTPException
from sqlalchemy.orm import Session
from dataBase import engine,get_db,Base,PostResponse,PostCreate
from Table import Post
from typing import List



# Correct table creation
Base.metadata.create_all(bind=engine)

app = FastAPI()

#Insert new data into table
@app.post("/insertdata",response_model=PostResponse,status_code=status.HTTP_201_CREATED)
def InsertData(post:PostCreate,db: Session = Depends(get_db)):
    #In a backend it perform SQL query
    new_data=Post(id=post.id,name=post.name,topic=post.topic)
    #new_data=Post(**post.dict()) this is same to above
    #add in the database
    db.add(new_data)
    #Commit
    db.commit()
    #Refresh the database
    db.refresh(new_data)
    return new_data

# ✅ Get all data
@app.get("/DB", response_model=List[PostResponse])
def get_database(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

# Get the single id
@app.get("/Get_by_id/{id}", response_model=PostResponse)
def single_id(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()  # must call .first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} was not found"
        )
    return post

# Delete the row
@app.delete("/delete/{id}",response_model=PostResponse)
def delete(id:int, db: Session = Depends(get_db)):
    post =db.query(Post).filter(Post.id== id).first()

    if not post :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} was not found"
        )
    db.delete(post)
    db.commit()
    return post

#Update the post
@app.put("/update/{id}",response_model=PostResponse)
def update(id: int,update_post:PostCreate,db:Session=Depends(get_db)):
    post=db.query(Post).filter(Post.id==id).first()

    if not post:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} was not found"
        )
    post.name=update_post.name
    post.topic =update_post.topic

    db.commit()
    db.refresh(post)
    return post



