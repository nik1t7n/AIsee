from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from schemas.enums import VideoStatus
from schemas.user import UserResponse


# Обновленный класс Video
class VideoBase(BaseModel):
    upload_date: Optional[datetime]
    status: VideoStatus


class VideoCreate(VideoBase):
    user_id: int


class VideoResponse(VideoBase):
    id: int
    user: UserResponse
    # frames: List[Frame] = []

    class Config:
        orm_mode = True
