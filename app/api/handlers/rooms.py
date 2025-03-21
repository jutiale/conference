from fastapi import HTTPException
from sqlmodel import select
from app.api.deps import SessionDep
from app.api.models import Room
from app.api.schemas.rooms import RoomRead, RoomCreate


def read_rooms(session: SessionDep, skip: int, limit: int) -> list[RoomRead]:
    stmt = (select(Room).offset(skip).limit(limit))
    rooms = session.exec(stmt).all()
    return rooms


def create_room(session: SessionDep, room: RoomCreate):
    room_data = room.model_dump()
    room = Room(**room_data)
    session.add(room)
    session.commit()
    session.refresh(room)
    print(room)
    return room


def delete_room(session: SessionDep, room_id: int):
    room = session.exec(select(Room).where(Room.id == room_id)).first()
    if room.presentations:
        raise HTTPException(status_code=400, detail="There are presentations in this room")

    session.delete(room)
    session.commit()
    return True
