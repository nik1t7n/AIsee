from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, Date, Integer, String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from db.database import Base


class VideoStatus(str, Enum):
    completed = "completed"
    processing = "processing"


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    upload_date = Column(Date, default=datetime.now)
    status = Column(SQLAlchemyEnum(VideoStatus, name="video_status"), default=VideoStatus.processing)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Связь многие-ко-одному: Каждое видео принадлежит одному пользователю
    # user = relationship("User", back_populates="video", lazy="dynamic")

    # Связь один-ко-многим: Одно видео может иметь много кадров
    frames = relationship("Frame", back_populates="video", lazy="dynamic")

    # Связь один-ко-одному: одно видео может иметь только один результат
    analysis_results = relationship("AnalysisResult", back_populates="video", lazy="dynamic")

