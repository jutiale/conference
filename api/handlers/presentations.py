from fastapi import HTTPException
from sqlmodel import select

from api.deps import SessionDep, CurrentUser
from api.models import Presentation, UserReport, UserPresentation, Roles, Report
from api.schemas.presentations import PresentationRead, PresentationCreate, PresentationUpdate
from api.utils import get_user_report, get_presentation_for_presenter


def read_presentations(session: SessionDep, user_id: int, skip: int, limit: int):
    user_presentations = session.exec(
        select(UserPresentation).where(UserPresentation.user_id == user_id).offset(skip).limit(limit)
    ).all()

    presentations = []
    for up in user_presentations:
        presentation = up.presentation
        presentations.append(PresentationRead(**presentation.model_dump(), role=up.user_role.value))

    return presentations


def create_presentation(session: SessionDep, presentation: PresentationCreate, user_id: int):
    # Access check
    report = get_user_report(session, presentation.report_id, user_id)

    overlapping_presentation = session.exec(select(Presentation).where(
            Presentation.room_id == presentation.room_id,
            Presentation.time_start < presentation.time_end, Presentation.time_end > presentation.time_start)
    ).first()
    if overlapping_presentation:
        raise HTTPException(
            status_code=400,
            detail="Time overlap in this room"
        )

    presentation_data = presentation.model_dump()
    new_presentation = Presentation(**presentation_data)
    session.add(new_presentation)
    session.flush()
    session.refresh(new_presentation)

    # Add all report authors to presentation
    users_reports = session.exec(select(UserReport).where(UserReport.report_id == report.id)).all()
    for user in users_reports:
        user_presentation = UserPresentation(user_id=user.user_id, presentation_id=new_presentation.id,
                                             user_role=Roles.presenter)
        session.add(user_presentation)

    session.commit()

    return PresentationRead(
        id=new_presentation.id,
        report_id=new_presentation.report_id,
        time_start=new_presentation.time_start,
        time_end=new_presentation.time_end,
        room_id=new_presentation.room_id,
        role=Roles.presenter.name
    )


def get_presentation_by_id(session: SessionDep, presentation_id: int, user_id: int):
    presentation = session.get(Presentation, presentation_id)
    if not presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")

    user_presentation = session.exec(
        select(UserPresentation).where(UserPresentation.user_id == user_id,
                                       UserPresentation.presentation_id == presentation_id)
    ).first()
    if not user_presentation:
        raise HTTPException(status_code=403, detail="Access denied")

    return PresentationRead(
        id=presentation.id,
        report_id=presentation.report_id,
        time_start=presentation.time_start,
        time_end=presentation.time_end,
        room_id=presentation.room_id,
        role=user_presentation.user_role
    )


def update_presentation(session: SessionDep, presentation_id: int, user_id: int, presentation_in: PresentationUpdate):
    presentation = get_presentation_for_presenter(session, presentation_id, user_id)

    update_dict = presentation_in.model_dump(exclude_unset=True)
    presentation.sqlmodel_update(update_dict)
    session.add(presentation)
    session.commit()
    session.refresh(presentation)

    return PresentationRead(
        id=presentation.id,
        report_id=presentation.report_id,
        time_start=presentation.time_start,
        time_end=presentation.time_end,
        room_id=presentation.room_id,
        role=Roles.presenter.value
    )


def delete_presentation(session: SessionDep, presentation_id: int, user_id: int):
    presentation = get_presentation_for_presenter(session, presentation_id, user_id)
    session.delete(presentation)
    session.commit()
    return True
