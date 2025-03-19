from typing import Any
from fastapi import APIRouter
from api.deps import CurrentUser, SessionDep
from api.handlers import rooms
from api.schemas.rooms import RoomRead, RoomCreate

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("/", summary="Получить аудитории", response_model=list[RoomRead])
def read_rooms(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve rooms.
    """
    return rooms.read_rooms(session, skip, limit)


@router.post("/", summary="Создать аудиторию", response_model=RoomRead)
def create_room(
    *, session: SessionDep, current_user: CurrentUser, room_in: RoomCreate
) -> Any:
    """
    Create new room.
    """
    return rooms.create_room(session, room_in)


@router.delete("/{room_id}", summary="Удалить аудиторию")
def delete_room(
    session: SessionDep, current_user: CurrentUser, room_id: int
) -> Any:
    """
    Delete a room.
    """
    return rooms.delete_room(session, room_id)
