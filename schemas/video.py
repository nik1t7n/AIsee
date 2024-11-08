from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from schemas.analysis_result import AnalysisResult
from schemas.enums import VideoStatus
from schemas.frame import Frame
from schemas.user import UserResponse


# Обновленный класс Video
class VideoBase(BaseModel):
    upload_date: Optional[datetime]
    status: VideoStatus


class VideoCreate(VideoBase):
    user_id: int


class Video(VideoBase):
    id: int
    user: UserResponse
    frames: List[Frame] = []  # Список кадров
    analysis_result: Optional[AnalysisResult] = None  # Один результат анализа

    class Config:
        orm_mode = True
