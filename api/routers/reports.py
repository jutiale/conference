import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from api.deps import CurrentUser, SessionDep
from api.models import Report
from api.schemas.reports import ReportRead, ReportCreate, ReportUpdate
from api.handlers import reports

router = APIRouter(prefix="/report", tags=["reports"])


@router.get("/", response_model=list[ReportRead])
def read_reports(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items.
    """
    return reports.read_reports(session, current_user.id, skip, limit)


@router.get("/{report_id}", response_model=ReportRead)
def read_report(session: SessionDep, current_user: CurrentUser, report_id: int) -> Any:
    """
    Get report by ID.
    """
    return reports.get_report_by_id(session, report_id, current_user.id)


@router.post("/", response_model=ReportRead)
def create_report(
    *, session: SessionDep, current_user: CurrentUser, report_in: ReportCreate
) -> Any:
    """
    Create new report.
    """
    return reports.create_report(session, report_in, current_user.id)


@router.put("/{report_id}", response_model=ReportRead)
def update_report(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    report_id: int,
    report_in: ReportUpdate,
) -> Any:
    """
    Update a report.
    """

    return reports.update_report(session, report_id, current_user.id, report_in)


@router.delete("/{report_id}")
def delete_report(
    session: SessionDep, current_user: CurrentUser, report_id: int
) -> Any:
    """
    Delete a report.
    """
    return reports.delete_report(session, report_id, current_user.id)