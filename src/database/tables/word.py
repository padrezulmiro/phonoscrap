from sqlalchemy import Column, Integer, String
from src.database import Base


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    ortho = Column(String)
