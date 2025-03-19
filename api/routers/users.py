from typing import Any

from fastapi import APIRouter, HTTPException

from api.handlers import users, login
from api.schemas.users import UserRead, UserRegister
from api.deps import (
    CurrentUser,
    SessionDep,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=UserRead)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user
    """
    user = login.get_user_by_name(session=session, name=user_in.name)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this name already exists in the system",
        )
    user_create = UserRegister.model_validate(user_in)
    user = users.create_user(session=session, user_create=user_create)
    return user


@router.get("/me", response_model=UserRead)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user
