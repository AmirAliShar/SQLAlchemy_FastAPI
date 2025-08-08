from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String, Integer,Boolean,DateTime,TIMESTAMP
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

password=os.environ.get("password")
host=os.environ.get("host")
database=os.environ.get("database")

# For connecting database
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
    
#Create the table

class SchemaTable(Base):
    __tablename__="Posts"
    id=Column(Integer,primary_key=True,nullable=False,index=True, autoincrement=True)
    name=Column(String,nullable=False)
    title=Column(String,nullable=False)
    published=Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ Add this
