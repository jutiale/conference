from datetime import time

from sqlmodel import Field, Relationship, SQLModel


class PresentationCreate(SQLModel):
    report_id: int
    time_start: time
    time_end: time
    room_id: int


class PresentationRead(PresentationCreate):
    id: int
    # role: str  # User role in this presentation


class PresentationUpdate(SQLModel):
    report_id: int
    time_start: time
    time_end: time
    room_id: int

