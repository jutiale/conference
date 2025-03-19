import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from api.handlers import users
from api.schemas import UserRead, UserRegister
from api.deps import (
    CurrentUser,
    SessionDep,
)
from api.config import settings
from api.security import get_password_hash, verify_password
from api.models import (
    User
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=UserRead)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user
    """
    # user = crud.get_user_by_email(session=session, email=user_in.email)
    # if user:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="The user with this email already exists in the system",
    #     )
    user_create = UserRegister.model_validate(user_in)
    user = users.create_user(session=session, user_create=user_create)
    return user


@router.get("/me", response_model=UserRead)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user
