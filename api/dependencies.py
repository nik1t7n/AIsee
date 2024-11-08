from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from repositories.analysis import AnalysisRepository
from repositories.frame import FrameRepository
from repositories.user import UserRepository
from repositories.video import VideoRepository
from services.auth import AuthenticationService
from services.user import UserService
from services.video import VideoService


def get_user_repository(
        conn: AsyncSession = Depends(get_db)
) -> UserRepository:
    return UserRepository(conn)

def get_video_repository(
        conn: AsyncSession = Depends(get_db)
) -> VideoRepository:
    return VideoRepository(conn)

def get_frame_repository(
        conn: AsyncSession = Depends(get_db)
) -> FrameRepository:
    return FrameRepository(conn)

def get_analysis_repository(
        conn: AsyncSession = Depends(get_db)
) -> AnalysisRepository:
    return AnalysisRepository(conn)

def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository)


def get_auth_service(
        user_service: UserService = Depends(get_user_service)
) -> AuthenticationService:
    return AuthenticationService(user_service)


def get_video_service(
        video_repository: VideoRepository = Depends(get_video_repository),
        frame_repository: FrameRepository = Depends(get_frame_repository),
        analysis_repository: AnalysisRepository = Depends(get_analysis_repository)
) -> VideoService:
    return VideoService(video_repository, frame_repository, analysis_repository)