from typing import List

from sqlalchemy import select

from models.frame import Frame
from repositories.base import BaseRepository
from schemas.frame import FrameCreate


class FrameRepository(BaseRepository):

    async def create_frame(self, frame: FrameCreate) -> Frame:
        async with self.connection as session:
            db_frame = Frame(
                video_id=frame.video_id,
                frame_number=frame.frame_number,
                timestamp=frame.timestamp,
                analysis_data=frame.analysis_data
            )
            session.add(db_frame)
            await session.commit()
            await session.refresh(db_frame)
            return db_frame

    async def create_frames_batch(self, frames: List[FrameCreate]) -> List[Frame]:
        async with self.connection as session:
            db_frames = [
                Frame(
                    video_id=frame.video_id,
                    frame_number=frame.frame_number,
                    timestamp=frame.timestamp,
                    analysis_data=frame.analysis_data
                )
                for frame in frames
            ]
            session.add_all(db_frames)
            await session.commit()
            for frame in db_frames:
                await session.refresh(frame)
            return db_frames

    async def get_video_frames(self, video_id: int) -> List[Frame]:
        async with self.connection as session:
            result = await session.execute(
                select(Frame).filter(Frame.video_id == video_id)
                .order_by(Frame.frame_number)
            )
            return result.scalars().all()
