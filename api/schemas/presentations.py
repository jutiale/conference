from datetime import datetime

from sqlmodel import SQLModel


class PresentationCreate(SQLModel):
    report_id: int
    time_start: datetime
    time_end: datetime
    room_id: int


class PresentationRead(PresentationCreate):
    id: int


class PresentationUpdate(SQLModel):
    report_id: int
    time_start: datetime
    time_end: datetime
    room_id: int

