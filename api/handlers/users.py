import uuid
from typing import Any

from sqlmodel import Session, select

from api.security import get_password_hash, verify_password
from api.models import User
from api.schemas import UserRegister


def create_user(*, session: Session, user_create: UserRegister) -> User:
    db_obj = User.model_validate(
        user_create, update={"password_hash": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
