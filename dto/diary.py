import datetime
from pydantic import BaseModel
from dto.plan import Plan_Base, Plan_Response

class Diary_Base(BaseModel):
    user_id: int
    date: datetime.date
    created_at: datetime.datetime

class Diary_Create_Request(Diary_Base):
    plan_list: list[Plan_Base]

class Diary_Update_Request(Diary_Base):
    content: str

class Diary_Response(Diary_Base):
    id: int
    content: str
    plan_list: list[Plan_Response]

class Diary_Message_Response(BaseModel):
    message: str