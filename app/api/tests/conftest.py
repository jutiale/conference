from typing import Generator
import pytest
from faker import Faker
from sqlmodel import Session, SQLModel
from fastapi.testclient import TestClient

from app.api.config import settings
from app.api.db import engine
from app.api.handlers.reports import create_report
from app.api.models import User, Room, Report
from app.api.schemas.presentations import PresentationCreate
from app.api.schemas.reports import ReportCreate
from app.api.schemas.rooms import RoomCreate
from app.api.schemas.users import UserRegister
from app.main import app
from app.api.tests.utils import authentication_token_from_name, create_room, create_random_password, create_presentation, \
    create_user

fake = Faker()


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        SQLModel.metadata.create_all(engine)
        yield session
        session.close()
        SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_name(
        client=client, name=fake.name(), session=db
    )


@pytest.fixture(scope="function")
def setup_test_data_room(db: Session) -> Room:
    room_data = RoomCreate(name=fake.word())
    room = create_room(db, room_data)
    return room


@pytest.fixture(scope="function")
def setup_test_data_user(db: Session) -> User:
    name = settings.NAME_TEST_USER
    password = create_random_password()
    user_in = UserRegister(name=name, password=password)
    user = create_user(session=db, user_create=user_in)
    return user


@pytest.fixture
def setup_test_data_report(db: Session, setup_test_data_user: User, setup_test_data_room: Room) -> Report:
    report_data = ReportCreate(
        name=fake.sentence(),
        text=fake.text(),
        user_id=setup_test_data_user.id,
        room_id=setup_test_data_room.id,
    )
    report = create_report(db, report_data, user_id=setup_test_data_user.id)
    return report


@pytest.fixture
def setup_test_data_presentation(db: Session, setup_test_data_report: Report):
    presentation_data = PresentationCreate(room_id=1, report_id=1, time_start="2025-03-20T09:30:00",
                                           time_end="2025-03-20T10:00:00")
    presentation = create_presentation(db, presentation_data, user_id=1)
    return presentation
