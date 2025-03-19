from sqlmodel import SQLModel


class UserRead(SQLModel):
    name: str


class UserRegister(SQLModel):
    password: str
    name: str
