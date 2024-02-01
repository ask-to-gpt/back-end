import datetime
from sqlalchemy.orm import Session
from ..dto.chat_room import Chat_Room_Base
from ..model.chat import Chat_Room, Chat

class Chat_Room_Service:
    def __init__(self) -> None:
        pass

    def create_room(self, db: Session, chat_room_request: Chat_Room_Base) -> Chat_Room:
        room = Chat_Room(
            user_id=chat_room_request.user_id,
            date=chat_room_request.date,
            created_at=datetime.datetime.now()
        )
        db.add(room)
        db.commit()
        return room

    def delete_room(self, db: Session, room_id: int) -> str:
        room = db.query(Chat_Room).get(room_id)
        db.delete(room)
        db.commit()
        return "삭제되었습니다."