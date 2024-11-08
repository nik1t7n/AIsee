from sqlalchemy import select

from models.analysis_result import AnalysisResult
from repositories.base import BaseRepository
from schemas.analysis_result import AnalysisResultCreate


class AnalysisRepository(BaseRepository):

    async def create_result(self, result: AnalysisResultCreate) -> AnalysisResult:
        async with self.connection as session:
            db_result = AnalysisResult(
                video_id=result.video_id,
                result_type=result.result_type,
                data=result.data,
                created_at=result.created_at
            )
            session.add(db_result)
            await session.commit()
            await session.refresh(db_result)
            return db_result

    async def get_by_video_id(self, video_id: int) -> AnalysisResult | None:
        async with self.connection as session:
            result = await session.execute(
                select(AnalysisResult).filter(AnalysisResult.video_id == video_id)
            )
            return result.scalars().first()