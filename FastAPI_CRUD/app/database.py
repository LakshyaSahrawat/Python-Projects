"""Database connection and session factory."""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config_layer.config import DATABASE_URL

# Ensure async DB URL (for SQLite: sqlite+aiosqlite:///, for Postgres: postgresql+asyncpg://)
ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)