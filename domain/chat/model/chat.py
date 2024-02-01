from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Chat_Room(Base):
    __tablename__ = "chat_room"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    date = Column(Date)
    created_at = Column(DateTime)
    chats = relationship("Chat", back_populates="room", cascade="delete")

class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer) # 0이면 AI
    content = Column(String(512))
    created_at = Column(DateTime)
    room_id = Column(Integer, ForeignKey("chat_room.id"))
    room = relationship("Chat_Room", back_populates="chats")