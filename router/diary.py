from fastapi import APIRouter, Depends
from langchain_community.chat_models import ChatOpenAI
from sqlalchemy.orm import Session
from db import get_db
from service.diary import Diary_Service
from dto.diary import (
    Diary_Create_Request, Diary_Update_Request, 
    Diary_Response, Diary_Message_Response
)
from dto.plan import Plan_Response
from config.config import config

router = APIRouter(prefix="/diary")

diary_service = Diary_Service(ChatOpenAI(openai_api_key=config["OPENAI_API_KEY"]))

@router.post("", response_model=Diary_Response)
async def create_diary(diary_request: Diary_Create_Request, db: Session = Depends(get_db)):
    diary = diary_service.create_diary(diary_request, db)

    plan_list = []
    for plan in diary.plans:
        plan_dto = Plan_Response(
            id=plan.id,
            user_id=plan.user_id,
            content=plan.content,
            date=plan.date,
            start=plan.start,
            end=plan.end
        )
        plan_list.append(plan_dto)

    return Diary_Response(
        id=diary.id,
        user_id=diary.user_id,
        content=diary.content,
        date=diary.date,
        created_at=diary.created_at,
        plan_list=plan_list
    )

@router.post("/{id}", response_model=Diary_Response)
async def write_diary(id: int, db: Session = Depends(get_db)):
    diary = diary_service.write_diary(id, db)

    plan_list = []
    for plan in diary.plans:
        plan_dto = Plan_Response(
            id=plan.id,
            user_id=plan.user_id,
            content=plan.content,
            date=plan.date,
            start=plan.start,
            end=plan.end
        )
        plan_list.append(plan_dto)

    return Diary_Response(
        id=diary.id,
        user_id=diary.user_id,
        content=diary.content,
        date=diary.date,
        created_at=diary.created_at,
        plan_list=plan_list
    )

@router.get("/{id}", response_model=Diary_Response)
async def get_diary(id: int, db: Session = Depends(get_db)):
    diary = diary_service.get_diary(id, db)
    plan_list = []
    for plan in diary.plans:
        plan_dto = Plan_Response(
            id=plan.id,
            user_id=plan.user_id,
            content=plan.content,
            date=plan.date,
            start=plan.start,
            end=plan.end
        )
        plan_list.append(plan_dto)

    return Diary_Response(
        id=diary.id,
        user_id=diary.user_id,
        content=diary.content,
        date=diary.date,
        created_at=diary.created_at,
        plan_list=plan_list
    )

@router.patch("/{id}", response_model=Diary_Message_Response)
async def update_diary(id: int, diary_update_req: Diary_Update_Request, db: Session = Depends(get_db)):
    message = diary_service.update_diary(id, diary_update_req, db)
    return Diary_Message_Response(message=message)

@router.delete("/{id}", response_model=Diary_Message_Response)
async def delete_diary(id: int, db: Session = Depends(get_db)):
    message = diary_service.delete_diary(id, db)
    return Diary_Message_Response(message=message)