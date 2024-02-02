import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_community.chat_models import ChatOpenAI
from dto.chat import Chat_Request
from model import Chat, Diary
from config.config import config

class Chat_Service:
    def __init__(self, chatbot: ChatOpenAI) -> None:
        self.chatbot = chatbot

    def create_question(self, db: Session, chat_request: Chat_Request, diary_id:int) -> Chat:
        if chat_request.question_cnt >= int(config["QUESTION_LIMIT"]): # 다음 일정으로 넘어가기 직전.
            answer = "다음 일정을 입력해주세요."
        else:
            # 일기 존재여부
            diary = db.query(Diary).get(diary_id)
            if diary is None: 
                raise HTTPException(status_code=404, detail="일기가 존재하지 않습니다.")

            # 현재까지의 채팅내역 모두 모아 prompt 형식에 맞게 변경
            chat_list = diary.chats
            message_list = [SystemMessage(content=config["SYS_PROMPT"])] # add system message
            for chat in chat_list:
                message = HumanMessage(content=chat.content) if chat.user_id \
                    else AIMessage(content=chat.content)
                message_list.append(message)
            message_list.append(HumanMessage(content=chat_request.content))

            # get answer from chatbot
            answer = self.chatbot.invoke(message_list).content

        # db에 채팅 저장
        db_user_chat = Chat(
            user_id=chat_request.user_id, 
            content=chat_request.content, 
            diary_id=diary_id,
            created_at=chat_request.created_at
        )
        db_ai_chat = Chat(
            user_id=0,
            content=answer,
            diary_id=diary_id,
            created_at=datetime.datetime.now()
        )       
        self.__save_chat(db, db_user_chat, db_ai_chat)

        return db_ai_chat

    def get_contents(self, db: Session, diary_id: int) -> list[Chat]:
        if not self.__is_diary_exist(db, diary_id):
            raise HTTPException(status_code=404, detail="채팅방이 존재하지 않습니다.")

        chat_list = db.query(
            Chat.user_id, 
            Chat.content, 
            Chat.created_at
        ).filter(Chat.diary_id == diary_id).all()
        
        return chat_list

    def __is_diary_exist(self, db: Session, diary_id: int) -> bool:
        return db.query(Diary).get(diary_id) is not None

    def __save_chat(self, db: Session, *args) -> None:
        for chat in args:
            db.add(chat)
        db.commit()
        return