from fastapi import APIRouter, FastAPI

from api.main import api_router
from api.routers import users
from api.config import settings

app = FastAPI()

app.include_router(api_router, prefix="/api")
