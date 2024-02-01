from sqlalchemy import Integer, String, Date, DateTime, Column, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Diary(Base):
    __tablename__ = "diary"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(Text)
    date = Column(Date)
    created_at = Column(DateTime)