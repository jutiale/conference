from fastapi import HTTPException
from sqlalchemy import func
from sqlmodel import select

from api.deps import CurrentUser, SessionDep
from api.models import Report, UserReport
from api.schemas.reports import ReportRead, ReportCreate, ReportUpdate
from api.utils import get_user_report


def read_reports(session: SessionDep, current_user: CurrentUser, skip: int, limit: int) -> list[ReportRead]:
    stmt = (
        select(Report).join(UserReport).where(UserReport.user_id == current_user.id).offset(skip).limit(limit)
    )
    reports = session.exec(stmt).all()
    print(reports)
    return reports


def create_report(session: SessionDep, report: ReportCreate, user_id: int):
    report_data = report.model_dump()
    report = Report(**report_data, user_id=user_id)
    session.add(report)
    session.flush()
    session.refresh(report)
    user_report = UserReport(user_id=user_id, report_id=report.id)
    session.add(user_report)
    session.commit()
    session.refresh(report)
    return report


def get_report_by_id(session: SessionDep, report_id: int, user_id: int):
    return get_user_report(session, report_id, user_id)


def update_report(session: SessionDep, report_id: int, user_id: int, report_in: ReportUpdate):
    report = get_user_report(session, report_id, user_id)

    update_dict = report_in.model_dump(exclude_unset=True)
    report.sqlmodel_update(update_dict)
    session.add(report)
    session.commit()
    session.refresh(report)
    return report


def delete_report(session: SessionDep, report_id: int, user_id: int):
    report = get_user_report(session, report_id, user_id)
    session.delete(report)
    session.commit()
    return True
