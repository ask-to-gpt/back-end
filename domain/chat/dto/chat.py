from pydantic import BaseModel
from enums.topic import Topic
import datetime

class Chat(BaseModel):
    content: str
    created_at: datetime.datetime

class Chat_Request(Chat):
    topic: Topic