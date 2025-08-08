from sqlalchemy import Column, Integer, String
from dataBase import Base

class Post(Base):
    __tablename__ = "Post"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    topic = Column(String, nullable=False)
