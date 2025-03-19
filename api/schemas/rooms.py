from sqlmodel import SQLModel


class RoomCreate(SQLModel):
    name: str


class RoomRead(RoomCreate):
    id: int
