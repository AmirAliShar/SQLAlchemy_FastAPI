from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

password=os.environ.get("password")
host=os.environ.get("host")
database=os.environ.get("database")
# For connecting database
## db ="postgresql://<username>:<password>@<ip-address/hostname">/<DB name>

db_url =f"postgresql://postgres:{password}@{host}/{database}"

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from pydantic import BaseModel

class PostCreate(BaseModel):
    id: int
    name: str
    topic: str

class PostResponse(PostCreate):
    class Config:
        orm_mode = True
