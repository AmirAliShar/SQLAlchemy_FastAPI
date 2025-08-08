from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    name: str
    title:str
    published:bool=False
    

#Use the seperate schema for the create and update post
class CreatePost(PostBase): #Inheritate
    pass

class UpdatePost(PostBase):
    id:int
   
    

# Schema for returning model response
class ModelResponse(BaseModel):
    id:int
    name: str
    title: str
    published: bool
    created_at: datetime

    class Config:  # ✅ Capital C
        orm_mode = True  # This will till the pydantic Model to read the data even if not a dict