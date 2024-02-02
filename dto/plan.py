import datetime
from pydantic import BaseModel

class Plan_Base(BaseModel):
    user_id: int
    content: str
    date: datetime.date
    start: datetime.time
    end: datetime.time

class Plans_Create_Request(BaseModel):
    plan_list: list[Plan_Base]

class Plan_Response(Plan_Base):
    id: int