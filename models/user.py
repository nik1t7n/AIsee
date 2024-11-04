from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(Date)
    last_login = Column(Date)

    # Связь один-ко-многим: Один пользователь может иметь много видео
    videos = relationship("Video", back_populates="user")