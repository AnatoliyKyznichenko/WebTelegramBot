from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from app.core.config import settings

engine = create_async_engine(url=settings.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

