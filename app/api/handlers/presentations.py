from fastapi import HTTPException
from sqlmodel import select
from app.api.deps import SessionDep
from app.api.models import Presentation, UserReport, UserPresentation, Roles
from app.api.schemas.presentations import PresentationRead, PresentationCreate, PresentationUpdate
from app.api.utils import get_user_report, get_presentation_for_presenter, check_presentation_overlap


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

    check_presentation_overlap(session, presentation.room_id, presentation.time_start, presentation.time_end)

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
    session.refresh(new_presentation)

    return PresentationRead(**new_presentation.model_dump())


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

    return PresentationRead(**presentation.model_dump())


def update_presentation(session: SessionDep, presentation_id: int, user_id: int, presentation_in: PresentationUpdate):
    presentation = get_presentation_for_presenter(session, presentation_id, user_id)

    check_presentation_overlap(session, presentation.room_id, presentation.time_start, presentation.time_end)

    update_dict = presentation_in.model_dump(exclude_unset=True)
    presentation.sqlmodel_update(update_dict)
    session.add(presentation)
    session.commit()
    session.refresh(presentation)

    return PresentationRead(**presentation.model_dump())


def delete_presentation(session: SessionDep, presentation_id: int, user_id: int):
    presentation = get_presentation_for_presenter(session, presentation_id, user_id)
    session.delete(presentation)
    session.commit()
    return True


def sign_up_for_presentation(session: SessionDep, presentation_id: int, user_id: int):
    presentation = session.get(Presentation, presentation_id)
    if not presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")

    user_presentation = session.exec(
        select(UserPresentation).where(UserPresentation.user_id == user_id,
                                       UserPresentation.presentation_id == presentation_id)
    ).first()
    if user_presentation:
        raise HTTPException(status_code=400, detail="You are already signed up for this presentation")

    user_presentation = UserPresentation(user_id=user_id, presentation_id=presentation_id, user_role=Roles.listener)
    session.add(user_presentation)
    session.commit()
    session.refresh(user_presentation)

    return PresentationRead.model_validate(presentation)

