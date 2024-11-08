# routes/video.py
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_video_service
from schemas.frame import FrameCreate, FrameResponse
from schemas.video import VideoResponse
from services.video import VideoService

router = APIRouter()


@router.post("/videos/initialize", response_model=VideoResponse)
async def initialize_video_upload(
        user_id: int,
        total_frames: int,
        metadata: dict,
        service: VideoService = Depends(get_video_service)
):
    """Инициализация загрузки видео"""
    try:
        return await service.initialize_video(user_id, total_frames, metadata)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/videos/{video_id}/frames/batch")
async def upload_frames_batch(
        video_id: int,
        frames_batch: FrameResponse,
        service: VideoService = Depends(get_video_service)
):
    """Загрузка батча фреймов"""
    try:
        await service.process_frames_batch(video_id, frames_batch)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/videos/{video_id}/complete")
async def complete_video_upload(
        video_id: int,
        service: VideoService = Depends(get_video_service)
):
    """Завершение загрузки видео и запуск анализа"""
    try:
        result = await service.complete_video_processing(video_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/videos/{video_id}/status")
async def get_video_status(
        video_id: int,
        service: VideoService = Depends(get_video_service)
):
    """Получение статуса обработки видео"""
    try:
        return await service.get_video_status(video_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
