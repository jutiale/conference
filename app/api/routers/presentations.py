from typing import Any
from fastapi import APIRouter
from app.api.deps import CurrentUser, SessionDep
from app.api.schemas.presentations import PresentationRead, PresentationCreate, PresentationUpdate
from app.api.handlers import presentations

router = APIRouter(prefix="/presentations", tags=["presentations"])


@router.get("/", summary="Получить доступные презентации", response_model=list[PresentationRead])
def read_presentations(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get presentations
    """
    return presentations.read_presentations(session, current_user.id, skip, limit)


@router.get("/{presentation_id}", summary="Получить презентацию по id", response_model=PresentationRead)
def read_presentation(session: SessionDep, current_user: CurrentUser, presentation_id: int) -> Any:
    """
    Get presentation by ID.
    """
    return presentations.get_presentation_by_id(session, presentation_id, current_user.id)


@router.post("/", summary="Создать презентацию по докладу", response_model=PresentationRead)
def create_presentation(
    *, session: SessionDep, current_user: CurrentUser, report_in: PresentationCreate
) -> Any:
    """
    Create new presentation.
    """
    return presentations.create_presentation(session, report_in, current_user.id)


@router.put("/{presentation_id}", summary="Изменить презентацию", response_model=PresentationRead)
def update_presentation(
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


@router.delete("/{presentation_id}", summary="Удалить презентацию")
def delete_presentation(
    session: SessionDep, current_user: CurrentUser, presentation_id: int
) -> Any:
    """
    Delete a presentation.
    """
    return presentations.delete_presentation(session, presentation_id, current_user.id)


@router.post("/{presentation_id}/sign_up", summary="Зарегистрироваться слушателем на презентацию",
             response_model=PresentationRead)
def sign_up_for_presentation(
    *, session: SessionDep, current_user: CurrentUser, presentation_id: int
) -> Any:
    """
    Create new presentation.
    """
    return presentations.sign_up_for_presentation(session, presentation_id, current_user.id)
