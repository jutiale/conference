from fastapi import APIRouter

from app.api.routers import users
from app.api.routers import login
from app.api.routers import reports
from app.api.routers import presentations
from app.api.routers import rooms
from app.api.routers import schedule


api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(reports.router)
api_router.include_router(presentations.router)
api_router.include_router(rooms.router)
api_router.include_router(schedule.router)
