from fastapi import APIRouter
from api.routes import auth
from api.routes import video

api_router = APIRouter()


api_router.include_router(
    auth.router,
    tags=['Auth'],
    prefix="/auth"
)

api_router.include_router(
    video.router,
    tags=['Video'],
    prefix="/video"
)