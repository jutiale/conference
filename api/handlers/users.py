from sqlmodel import Session
from api.security import get_password_hash
from api.models import User
from api.schemas.users import UserRegister


def create_user(*, session: Session, user_create: UserRegister) -> User:
    db_obj = User.model_validate(
        user_create, update={"password_hash": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
