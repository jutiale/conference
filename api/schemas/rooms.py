from sqlmodel import Field, Relationship, SQLModel


class RoomCreate(SQLModel):
    name: str


class RoomRead(RoomCreate):
    id: int
