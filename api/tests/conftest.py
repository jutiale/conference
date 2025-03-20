from typing import Generator

import pytest
from faker import Faker
from sqlmodel import Session, SQLModel
from fastapi.testclient import TestClient
from api.db import engine
from api.handlers.reports import create_report
from api.models import User, Room
from api.schemas.reports import ReportCreate
from api.schemas.rooms import RoomCreate
from api.schemas.users import UserRegister
from api.utils import create_user
from main import app
from api.tests.utils import authentication_token_from_name, create_room, create_random_password

fake = Faker()


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        # init_db(session)
        # yield session
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
    name = fake.name()
    password = create_random_password()
    user_in = UserRegister(name=name, password=password)
    user = create_user(session=db, user_create=user_in)
    return user


@pytest.fixture
def setup_test_data_report(db: Session, setup_test_data_user: User, setup_test_data_room: Room):
    report_data = ReportCreate(
        name=fake.sentence(),
        text=fake.text(),
        user_id=setup_test_data_user.id,
        room_id=setup_test_data_room.id,
    )
    report = create_report(db, report_data, user_id=setup_test_data_user.id)
    return report
