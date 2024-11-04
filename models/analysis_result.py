from sqlalchemy import Boolean, Column, Date, Integer, String, ForeignKey, JSON, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from db.database import Base


from enum import Enum

class ResultType(str, Enum):
    staff = "Staff Analytics"
    space = "Space Analytics"
    customer = "Customer Analytics"


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    result_type = Column(SQLAlchemyEnum(ResultType, name="result_type"))
    data = Column(JSON)
    created_at = Column(Date)

    # Связь многие-ко-одному: Каждый результат анализа принадлежит одному видео
    video = relationship("Video", back_populates="analysis_results")
