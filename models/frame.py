from sqlalchemy import Boolean, Column, Date, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from db.database import Base


class Frame(Base):
    __tablename__ = "frames"

    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    frame_number = Column(Integer)
    timestamp = Column(Date)
    analysis_data = Column(JSON)

    # Связь многие-ко-одному: Каждый кадр принадлежит одному видео
    video = relationship("Video", back_populates="frames")