from fastapi import FastAPI,Depends, HTTPException,status
from sqlalchemy.orm import Session
from Database import Base,engine,get_db
from Schema import CreatePost,UpdatePost, ModelResponse
from Database import SchemaTable
from datetime import datetime
from typing import List
Base.metadata.create_all(bind=engine)
app=FastAPI()


#Insert the data
@app.post("/create", response_model=ModelResponse)
def data(post: CreatePost, db: Session = Depends(get_db)):
    new_post = SchemaTable(
        title=post.title,
        name=post.name,
        published=post.published,
        created_at=datetime.utcnow() 
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post  


# View the all data
@app.get("/view",response_model=List[ModelResponse]) # It is work will without ModelResponse but it return only output which we want
def Viewdata(db:Session=Depends(get_db)):
    post=db.query(SchemaTable).all()
    return post

#Retrive by id
@app.get("/posts/{id}",response_model=ModelResponse)
def SingleView(id:int,db:Session=Depends(get_db)):
    data=db.query(SchemaTable).filter(SchemaTable.id==id).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Id {id} not found")

    return data

# Update the row
@app.put("/Update/{id}",response_model=ModelResponse)
def Update(id:int,update:UpdatePost,db:Session=Depends(get_db)):
    data=db.query(SchemaTable).filter(SchemaTable.id==id).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Id {id} not found")
    
    data.name=update.name
    data.title=update.title
    data.published=update.published
    data.created_at=update.created_at
    db.commit()
    db.refresh(data)
    return data

@app.delete("/Delete/{id}",response_model=ModelResponse)
def deletePost(id:int,db:Session=Depends(get_db)):
    data=db.query(SchemaTable).filter(SchemaTable.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Id {id} not found")
    db.delete(data)
    db.commit()
    return data