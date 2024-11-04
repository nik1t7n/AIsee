from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import connection_string

# Create the declarative base before engine
Base = declarative_base()

# Create async engine
async_engine = create_async_engine(
    connection_string,
    echo=True,
)

# Create async session factory
SessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_all():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)