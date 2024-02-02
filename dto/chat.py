from pydantic import BaseModel
import datetime

class Chat_Base(BaseModel):
    user_id: int
    content: str
    created_at: datetime.datetime

class Chat_Request(Chat_Base):
    plan_id: int # 현재 질문 중인 일정
    question_cnt: int # 일정당 질문한 횟수 

class Chat_List_Response(BaseModel):
    chat_list: list[Chat_Base]