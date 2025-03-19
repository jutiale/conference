from fastapi import APIRouter

from api.routers import users
from api.routers import login
from api.config import settings

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(login.router)
