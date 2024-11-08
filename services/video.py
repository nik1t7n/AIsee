# services/video_service.py
from typing import List
import asyncio
from datetime import datetime
from models.video import VideoStatus, Video
from models.analysis_result import ResultType
from repositories.analysis import AnalysisRepository
from repositories.frame import FrameRepository
from repositories.video import VideoRepository
from schemas.analysis_result import AnalysisResultCreate
from schemas.frame import FrameCreate, FrameResponse
from schemas.video import VideoCreate


class VideoService:
    def __init__(
            self,
            video_repository: VideoRepository,
            frame_repository: FrameRepository,
            analysis_repository: AnalysisRepository
    ):
        self.video_repository = video_repository
        self.frame_repository = frame_repository
        self.analysis_repository = analysis_repository
        self.processing_videos = {}  # Cache for tracking progress

    async def initialize_video(
            self,
            user_id: int,
            total_frames: int,
            metadata: dict
    ) -> Video:
        video = await self.video_repository.create_video(
            VideoCreate(user_id=user_id)
        )

        self.processing_videos[video.id] = {
            'total_frames': total_frames,
            'processed_frames': 0,
            'metadata': metadata
        }

        return Video(
            upload_id=video.id,
            status=video.status
        )

    async def process_frames_batch(
            self,
            video_id: int,
            frames_batch: FrameResponse
    ) -> None:
        if video_id not in self.processing_videos:
            raise ValueError("Video upload not initialized")

        # Создаем задачи для параллельного анализа фреймов
        analysis_tasks = []
        for frame in frames_batch.frames:
            task = asyncio.create_task(self.analyze_frame(frame))
            analysis_tasks.append(task)

        # Ждем выполнения всех задач анализа
        frame_results = await asyncio.gather(*analysis_tasks)

        # Создаем объекты FrameCreate для каждого проанализированного фрейма
        frames_to_create = [
            FrameCreate(
                video_id=video_id,
                frame_number=frame.frame_number,
                timestamp=frame.timestamp,
                analysis_data=analysis_result
            )
            for frame, analysis_result in zip(frames_batch.frames, frame_results)
        ]

        # Сохраняем все фреймы одним батчем
        await self.frame_repository.create_frames_batch(frames_to_create)

        # Обновляем прогресс
        self.processing_videos[video_id]['processed_frames'] += len(frames_batch.frames)

    async def analyze_frame(self, frame_data: dict) -> dict:
        # Здесь должна быть ваша логика анализа кадра
        # Это заглушка для примера
        await asyncio.sleep(0.1)  # Имитация асинхронной обработки
        return {
            "detected_objects": [],
            "movement_analysis": {},
            "occupancy_data": {}
        }

    def aggregate_analysis(self, frames_data: List[dict]) -> dict:
        # Здесь должна быть ваша логика агрегации результатов
        # Это заглушка для примера
        return {
            "total_frames": len(frames_data),
            "average_occupancy": 0,
            "peak_activity_times": [],
            "summary": {}
        }

    async def complete_video_processing(self, video_id: int) -> dict:
        if video_id not in self.processing_videos:
            raise ValueError("Video not found")

        video_data = self.processing_videos[video_id]
        if video_data['processed_frames'] < video_data['total_frames']:
            raise ValueError("Not all frames have been processed")

        # Получаем все фреймы видео
        frames = await self.frame_repository.get_video_frames(video_id)

        # Агрегируем результаты анализа
        final_analysis = self.aggregate_analysis([frame.analysis_data for frame in frames])

        # Создаем итоговый результат анализа
        analysis_result = await self.analysis_repository.create_result(
            AnalysisResultCreate(
                video_id=video_id,
                result_type=ResultType.staff,
                data=final_analysis,
                created_at=datetime.now()
            )
        )

        # Обновляем статус видео
        await self.video_repository.update_status(video_id, VideoStatus.completed)

        # Очищаем кеш
        del self.processing_videos[video_id]

        return final_analysis

    async def get_video_status(self, video_id: int) -> dict:
        video = await self.video_repository.get_by_id(video_id)
        if not video:
            raise ValueError("Video not found")

        progress = None
        if video_id in self.processing_videos:
            video_data = self.processing_videos[video_id]
            progress = (video_data['processed_frames'] / video_data['total_frames']) * 100

        return {
            "status": video.status,
            "progress": progress
        }