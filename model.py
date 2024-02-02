from sqlalchemy import (
    Column, ForeignKey, Integer, Boolean,
    String, DateTime, Date, TEXT, Time
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Diary(Base):
    __tablename__ = "diary"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(TEXT)
    date = Column(Date)
    created_at = Column(DateTime)
    chats = relationship("Chat", back_populates="diary", cascade="delete")
    plans = relationship("Plan", back_populates="diary", cascade="delete")

class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer) # 0이면 AI
    content = Column(String(512))
    created_at = Column(DateTime)
    diary_id = Column(Integer, ForeignKey("diary.id"))
    diary = relationship("Diary", back_populates="chats")

class Plan(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(String(255))
    date = Column(Date)
    start = Column(Time)
    end = Column(Time)
    diary_id = Column(Integer, ForeignKey("diary.id"))
    diary = relationship("Diary", back_populates="plans")