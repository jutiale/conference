from datetime import datetime
from typing import List

from sqlmodel import SQLModel


class PresentationSchedule(SQLModel):
    id: int
    report_id: int
    time_start: datetime
    time_end: datetime


class RoomSchedule(SQLModel):
    room_id: int
    room_name: str
    presentations: List[PresentationSchedule]