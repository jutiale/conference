from typing import Type

from fastapi import HTTPException
from sqlmodel import Session, select

from api.models import Report, UserReport, Presentation, UserPresentation, Roles, User
from api.schemas.users import UserUpdate, UserRegister
from api.security import get_password_hash


def get_user_report(session: Session, report_id: int, user_id: int) -> Type[Report]:
    """
    Gets a report by id and checks if user has an access.
    If report not found — 404.
    If user has no rights — 403.
    """
    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    user_report = session.exec(
        select(UserReport).where(UserReport.user_id == user_id, UserReport.report_id == report_id)
    ).first()
    if not user_report:
        raise HTTPException(status_code=403, detail="Access denied")

    return report


def get_presentation_for_presenter(session: Session, presentation_id: int, user_id: int) -> Type[Presentation]:
    """
    Gets a presentation by id and checks if user is a presenter.
    If presentation not found — 404.
    If user has no rights — 403.
    """
    user_presentation = session.exec(
        select(UserPresentation).where(UserPresentation.user_id == user_id,
                                       UserPresentation.presentation_id == presentation_id)
    ).first()
    if not user_presentation or user_presentation.user_role != Roles.presenter:
        raise HTTPException(status_code=403, detail="Access denied")

    return user_presentation.presentation


def update_user(*, session: Session, db_user: User, user_in: UserUpdate):
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def create_user(*, session: Session, user_create: UserRegister) -> User:
    db_obj = User.model_validate(
        user_create, update={"password_hash": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
