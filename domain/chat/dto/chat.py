from pydantic import BaseModel
from enums.topic import Topic
import datetime

class Chat_Base(BaseModel):
    user_id: int
    content: str
    created_at: datetime.datetime

class Chat_Request(Chat_Base):
    plan_finished: bool

class Chat_List_Response(BaseModel):
    chat_list: list[Chat_Base]