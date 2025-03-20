from sqlmodel import SQLModel


class ReportCreate(SQLModel):
    name: str
    text: str


class ReportRead(ReportCreate):
    id: int


class ReportUpdate(SQLModel):
    name: str
    text: str
