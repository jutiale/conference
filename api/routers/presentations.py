import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from api.deps import CurrentUser, SessionDep
from api.models import Report
from api.schemas.presentations import PresentationRead, PresentationCreate, PresentationUpdate
from api.handlers import presentations

router = APIRouter(prefix="/presentations", tags=["presentations"])


@router.get("/", response_model=list[PresentationRead])
def read_presentations(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get presentations
    """
    return presentations.read_presentations(session, current_user.id, skip, limit)


@router.get("/{presentation_id}", response_model=PresentationRead)
def read_presentattion(session: SessionDep, current_user: CurrentUser, presentation_id: int) -> Any:
    """
    Get presentation by ID.
    """
    return presentations.get_presentation_by_id(session, presentation_id, current_user.id)


@router.post("/", response_model=PresentationRead)
def create_presentation(
    *, session: SessionDep, current_user: CurrentUser, report_in: PresentationCreate
) -> Any:
    """
    Create new presentation.
    """
    return presentations.create_presentation(session, report_in, current_user.id)


@router.put("/{presentation_id}", response_model=PresentationRead)
def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    presentation_id: int,
    presentation_in: PresentationUpdate,
) -> Any:
    """
    Update a presentation.
    """

    return presentations.update_presentation(session, presentation_id, current_user.id, presentation_in)

#
# @router.delete("/{report_id}")
# def delete_item(
#     session: SessionDep, current_user: CurrentUser, report_id: int
# ) -> Any:
#     """
#     Delete a report.
#     """
#     return reports.delete_report(session, report_id, current_user.id)