from sqlalchemy import select, update

from models.video import Video
from repositories.base import BaseRepository
from schemas.enums import VideoStatus
from schemas.video import VideoCreate


class VideoRepository(BaseRepository):

    async def create_video(self, video: VideoCreate) -> Video:
        async with self.connection as session:
            db_video = Video(
                user_id=video.user_id,
                status=VideoStatus.processing
            )
            session.add(db_video)
            await session.commit()
            await session.refresh(db_video)
            return db_video

    async def get_by_id(self, video_id: int) -> Video | None:
        async with self.connection as session:
            result = await session.execute(
                select(Video).filter(Video.id == video_id)
            )
            return result.scalars().first()

    async def update_status(self, video_id: int, status: VideoStatus) -> Video:
        async with self.connection as session:
            stmt = update(Video).where(Video.id == video_id).values(status=status)
            await session.execute(stmt)
            await session.commit()

            # Получаем обновленное видео
            result = await session.execute(
                select(Video).filter(Video.id == video_id)
            )
            return result.scalars().first()