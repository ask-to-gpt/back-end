from fastapi import APIRouter
from .service import Chat_Service
from .dto.chat import Chat, Chat_Request
from llm.prompt import Custom_Prompt
import datetime

router = APIRouter(prefix="/chat")

chat_service = Chat_Service(prompt=Custom_Prompt())

@router.post("/")
async def chat(chat_request: Chat_Request) -> Chat:
    answer = chat_service.get_answer(chat_request)
    res = Chat(content=answer, created_at=datetime.datetime.now())
    return res