from typing import Any
from fastapi import APIRouter
from app.api.deps import CurrentUser, SessionDep
from app.api.handlers import schedule
from app.api.schemas.schedule import RoomSchedule

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.get("/", summary="Получить расписание презентаций, разбитое по аудиториям",
            response_model=list[RoomSchedule])
def read_schedule(
    session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get schedule grouped by rooms
    """
    return schedule.read_schedule(session)
