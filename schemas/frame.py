# Схема для кадров
from datetime import datetime

from pydantic import BaseModel

from schemas.video import VideoResponse


class FrameBase(BaseModel):
    frame_number: int
    timestamp: datetime
    analysis_data: dict  # Анализ данных в формате JSON


class FrameCreate(FrameBase):
    video_id: int


class FrameResponse(FrameBase):
    id: int
    video: VideoResponse  # Ссылка на видео

    class Config:
        orm_mode = True
