# Схема для пользователя
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    company_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    company_name: Optional[str]
    email: Optional[EmailStr]


class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        orm_mode = True
