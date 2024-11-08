# Схема для результатов анализа
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.enums import ResultType
from schemas.video import VideoResponse


class AnalysisResultBase(BaseModel):
    result_type: ResultType
    data: dict  # Данные результата в формате JSON
    created_at: Optional[datetime]


class AnalysisResultCreate(AnalysisResultBase):
    video_id: int


class AnalysisResultResponse(AnalysisResultBase):
    id: int
    video: VideoResponse  # Ссылка на видео

    class Config:
        orm_mode = True
