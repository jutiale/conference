import enum
import uuid
from datetime import time
from typing import Annotated, Union

# from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship


class Roles(enum.Enum):
    presenter = 'presenter'
    listener = 'listener'
    admin = 'admin'


class UserReport(SQLModel, table=True):
    __tablename__ = "users_reports"

    id: Union[int, None] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    report_id: int = Field(foreign_key="reports.id", ondelete="CASCADE")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Union[int, None] = Field(default=None, primary_key=True)
    name: str
    password_hash: str


class Report(SQLModel, table=True):
    __tablename__ = "reports"

    id: Union[int, None] = Field(default=None, primary_key=True)
    name: str
    text: str


class Room(SQLModel, table=True):
    __tablename__ = "rooms"

    id: Union[int, None] = Field(default=None, primary_key=True)
    name: str

    presentations: list["Presentation"] = Relationship(back_populates="room")


class Presentation(SQLModel, table=True):
    __tablename__ = "presentations"

    id: Union[int, None] = Field(default=None, primary_key=True)
    report_id: int = Field(foreign_key="reports.id", ondelete="CASCADE")
    time_start: time
    time_end: time
    room_id: int = Field(foreign_key="rooms.id")

    users_presentations: list["UserPresentation"] = Relationship(back_populates="presentation", cascade_delete=True)
    room: "Room" = Relationship(back_populates="presentations")


class UserPresentation(SQLModel, table=True):
    __tablename__ = "users_presentations"

    id: Union[int, None] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    presentation_id: int = Field(foreign_key="presentations.id", ondelete="CASCADE")
    user_role: Roles

    presentation: "Presentation" = Relationship(back_populates="users_presentations")

