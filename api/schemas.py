from sqlmodel import Field, Relationship, SQLModel


class UserRead(SQLModel):
    name: str


class UserRegister(SQLModel):
    password: str
    name: str
