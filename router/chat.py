from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from langchain_community.chat_models import ChatOpenAI
from service.chat import Chat_Service
from dto.chat import Chat_Base, Chat_Request, Chat_List_Response
from db import get_db
from config.config import config

router = APIRouter(prefix="/chat")

chat_service = Chat_Service(chatbot=ChatOpenAI(openai_api_key=config["OPENAI_API_KEY"]))

@router.get("/{diary_id}", response_model=Chat_List_Response)
async def get_chat(diary_id:int, db: Session = Depends(get_db)):
    chat_list = chat_service.get_contents(db, diary_id)
    res_list = [
        Chat_Base(
            user_id=chat.user_id, 
            content=chat.content, 
            created_at=chat.created_at
        ) for chat in chat_list
    ]
    return Chat_List_Response(chat_list=res_list)

@router.post("/{diary_id}", response_model=Chat_Base)
async def chat(diary_id: int, chat_request: Chat_Request, db: Session = Depends(get_db)):
    answer = chat_service.create_question(db, chat_request, diary_id)
    return Chat_Base(
        user_id=answer.user_id,
        content=answer.content, 
        created_at=answer.created_at
    )
