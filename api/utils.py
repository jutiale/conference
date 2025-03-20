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



