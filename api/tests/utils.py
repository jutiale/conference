import secrets
import string

from fastapi.testclient import TestClient
from sqlmodel import Session
from faker import Faker
from api.config import settings
from api.models import User, Report, Room
from api.handlers import login
from api.schemas.rooms import RoomCreate
from api.utils import update_user, create_user
from api.schemas.users import UserRegister, UserUpdate


def create_random_password():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))


def user_authentication_headers(
    *, client: TestClient, name: str, password: str
) -> dict[str, str]:
    data = {"username": name, "password": password}

    r = client.post(f"api/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_name(
    *, client: TestClient, name: str, session: Session
) -> dict[str, str]:
    """
    Return a valid token for the user with given name.

    If the user doesn't exist it is created first.
    """
    password = create_random_password()
    user = login.get_user_by_name(session=session, name=name)
    if not user:
        user_in_create = UserRegister(name=name, password=password)
        user = create_user(session=session, user_create=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        if not user.id:
            raise Exception("User id not set")
        user = update_user(session=session, db_user=user, user_in=user_in_update)

    return user_authentication_headers(client=client, name=name, password=password)


def create_random_user(session: Session) -> User:
    fake = Faker()
    name = fake.name()
    password = create_random_password()
    user_in = UserRegister(name=name, password=password)
    user = create_user(session=session, user_create=user_in)
    return user


def create_room(session: Session, room_in: RoomCreate) -> Room:
    room_data = room_in.model_dump()
    room = Room(**room_data)
    session.add(room)
    session.commit()
    session.refresh(room)
    return room

