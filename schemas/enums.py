# Определяем перечисления для статусов видео и типов результатов
from enum import Enum


class VideoStatus(str, Enum):
    completed = "completed"
    processing = "processing"


class ResultType(str, Enum):
    staff = "Staff Analytics"
    space = "Space Analytics"
    customer = "Customer Analytics"
