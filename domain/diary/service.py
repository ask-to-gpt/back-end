import datetime
from fastapi import HTTPException
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from sqlalchemy.orm import Session
from .dto.diary import Diary_Create_Request, Diary_Update_Request
from .model.diary import Diary
from domain.chat.model.chat import Chat
from config.config import config

class Diary_Service:
    def __init__(self, chatbot: ChatOpenAI):
        self.chatbot = chatbot

    def create_diary(self, diary_request: Diary_Create_Request, db: Session) -> Diary:
        if db.query(Diary).filter(Diary.date == diary_request.date).first():
            raise HTTPException(status_code=400, detail="이미 일기를 작성하셨습니다. 만약 다시 쓰고 싶으시다면 삭제 후 작성해주세요.")

        chat_list = db.query(Chat.user_id, Chat.content).filter(Chat.room_id == diary_request.room_id).all()
        diary_pormpt = config["DIARY_PROMPT"].format(diary_request.plan_list)

        message_list = [SystemMessage(content=config["SYS_PROMPT"])] # add system message
        for chat in chat_list:
            message = HumanMessage(content=chat.content) if chat.user_id \
                else AIMessage(content=chat.content)
            message_list.append(message)
        message_list.append(HumanMessage(content=diary_pormpt))

        # get answer from chatbot
        answer = self.chatbot.invoke(message_list).content

        db_diary = Diary(
            user_id=diary_request.user_id,
            content=answer,
            date=diary_request.date,
            created_at=datetime.datetime.now()
        )
        db.add(db_diary) 
        db.commit()

        return db_diary

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