from typing import Type

from fastapi import HTTPException
from sqlmodel import Session, select

from api.models import Report, UserReport


def get_user_report(session: Session, report_id: int, user_id: int) -> Type[Report]:
    """
    Gets a report by id and checks if user has an access.
    If report not founf — 404.
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
