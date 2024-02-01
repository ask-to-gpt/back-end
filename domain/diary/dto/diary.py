import datetime
from pydantic import BaseModel

class Diary_Base(BaseModel):
    user_id: int
    date: datetime.date

class Diary_Create_Request(Diary_Base):
    plan_list: list
    room_id: int

class Diary_Update_Request(Diary_Base):
    content: str

class Diary_Response(Diary_Base):
    id: int
    content: str
    created_at: datetime.datetime

class Diary_Message_Response(BaseModel):
    message: str