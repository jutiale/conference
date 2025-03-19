from fastapi import HTTPException
from sqlmodel import select

from api.deps import SessionDep, CurrentUser
from api.models import Presentation, UserReport, UserPresentation, Roles, Report
from api.schemas.presentations import PresentationRead, PresentationCreate
from api.utils import get_user_report


def read_presentations(session: SessionDep, user_id: int, skip: int, limit: int):
    user_presentations = session.exec(
        select(UserPresentation).where(UserPresentation.user_id == user_id)
    ).offset(skip).limit(limit)

    if not user_presentations:
        raise HTTPException(status_code=404, detail="No presentations found for this user")

    presentations = []
    for up in user_presentations:
        presentation = up.presentation
        presentations.append(PresentationRead(**presentation.model_dump(), role=up.user_role.value))

    return presentations


def create_presentation(session: SessionDep, presentation: PresentationCreate, user_id: int):
    # Access check
    user_report = get_user_report(session, presentation.report_id, user_id)

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
    users_reports = session.exec(select(UserReport).where(UserReport.report_id == user_report.report_id)).all()
    for user in users_reports:
        user_presentation = UserPresentation(user_id=user.user_id, presentation_id=new_presentation.id)
        session.add(user_presentation)

    session.commit()



# def get_report_by_id(session: SessionDep, report_id: int, user_id: int):
#     return get_user_report(session, report_id, user_id)
