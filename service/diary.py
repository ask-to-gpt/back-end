import datetime
from fastapi import HTTPException
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from sqlalchemy.orm import Session
from dto.diary import Diary_Create_Request, Diary_Update_Request
from model import Diary, Plan
from config.config import config

class Diary_Service:
    def __init__(self, chatbot: ChatOpenAI):
        self.chatbot = chatbot

    def create_diary(self, diary_request:Diary_Create_Request, db: Session) -> Diary:
        found_diary = db.query(Diary).filter(Diary.date == diary_request.date).first()
        if found_diary:
            raise HTTPException(status_code=400, detail="오늘 일기를 이미 작성하셨습니다.")
        if not len(diary_request.plan_list):
            raise HTTPException(status_code=400, detail="일정을 입력해주세요.")
        
        db_diary = Diary(
            user_id=diary_request.user_id,
            content="",
            date=diary_request.date,
            created_at=datetime.datetime.now()
        )
        db.add(db_diary)
        db.commit()

        for plan in diary_request.plan_list:
            db_plan = Plan(
                user_id=plan.user_id,
                content=plan.content,
                date=plan.date,
                start=plan.start,
                end=plan.end,
                diary_id=db_diary.id
            )
            db.add(db_plan)
        db.commit()

        return db_diary

    def write_diary(self, id: int, db: Session) -> Diary:
        diary = db.query(Diary).get(id)
        if diary is None:
            raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")
        if diary.content:
            raise HTTPException(status_code=400, detail="이미 일기를 작성하셨습니다. 만약 다시 쓰고 싶으시다면 삭제 후 작성해주세요.")

        chat_list = diary.chats
        plans_content = [(f"{plan.start.hour}:{plan.start.minute} ~ {plan.end.hour}:{plan.end.minute} {plan.content}") for plan in diary.plans]
        diary_prompt = config["DIARY_USER_PROMPT"].format(plans_content)
        print(diary_prompt)

        message_list = [SystemMessage(content=config["DIARY_SYS_PROMPT"])] # add system message
        for chat in chat_list:
            message = HumanMessage(content=chat.content) if chat.user_id \
                else AIMessage(content=chat.content)
            message_list.append(message)
        message_list.pop() # 마지막 AIMessage 제거
        message_list.append(HumanMessage(content=diary_prompt))

        # get answer from chatbot
        answer = self.chatbot.invoke(message_list).content

        diary.content = answer
        db.add(diary) 
        db.commit()

        return diary

    def get_diary(self, id: int, db: Session) -> Diary:
        diary = db.query(Diary).get(id)
        if diary is None:
            raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")
        return diary

    def update_diary(self, id: int, diary_update_req: Diary_Update_Request, db: Session) -> str:
        diary = self.get_diary(id, db)
        diary.content = diary_update_req.content
        db.add(diary)
        db.commit()
        return "수정되었습니다."


    def delete_diary(self, id: int, db: Session) -> str:
        diary = self.get_diary(id, db)
        db.delete(diary) 
        db.commit()
        return "삭제되었습니다."