# Схема для пользователя
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    company_name: str
    email: EmailStr


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        orm_mode = True
