from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from langchain_community.chat_models import ChatOpenAI
from .service.chat import Chat_Service
from .service.chat_room import Chat_Room_Service
from .dto.chat import Chat_Base, Chat_Request, Chat_List_Response
from .dto.chat_room import Chat_Room_Base, Chat_Room_Response, Chat_Room_Delete_Response
from db import get_db
from config.config import config

router = APIRouter(prefix="/chat")

chat_service = Chat_Service(chatbot=ChatOpenAI(openai_api_key=config["OPENAI_API_KEY"]))
chat_room_service = Chat_Room_Service()

@router.post("/room", status_code=201, response_model=Chat_Room_Response)
async def create_chat_room(
    room_request: Chat_Room_Base, 
    db: Session = Depends(get_db)):

    created_room = chat_room_service.create_room(db, room_request)
    room_dto = Chat_Room_Response(
        id=created_room.id,
        user_id=created_room.user_id,
        date=created_room.date,
        created_at=created_room.created_at
    )

    return room_dto

@router.get("/room/{id}", response_model=Chat_List_Response)
async def get_chat(id:int, db: Session = Depends(get_db)):
    chat_list = chat_service.get_contents(db, id)
    res_list = [
        Chat_Base(
            user_id=chat.user_id, 
            content=chat.content, 
            created_at=chat.created_at
        ) for chat in chat_list
    ]
    return Chat_List_Response(chat_list=res_list)

@router.post("/room/{id}", response_model=Chat_Base)
async def chat(id: int, chat_request: Chat_Request, db: Session = Depends(get_db)):
    answer = chat_service.create_question(db, chat_request, id)
    return Chat_Base(
        user_id=answer.user_id,
        content=answer.content, 
        created_at=answer.created_at
    )

@router.delete("/room/{id}", response_model=Chat_Room_Delete_Response)
async def delete_chat_room(id: int, db: Session = Depends(get_db)):
    message = chat_room_service.delete_room(db, id)
    return Chat_Room_Delete_Response(message=message)
