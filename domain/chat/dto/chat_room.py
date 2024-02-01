from pydantic import BaseModel
import datetime

class Chat_Room_Base(BaseModel):
    user_id: int
    date: datetime.date

class Chat_Room_Response(Chat_Room_Base):
    id: int
    created_at: datetime.datetime

class Chat_Room_Delete_Response(BaseModel):
    message: str