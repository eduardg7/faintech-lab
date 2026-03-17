"""Database configuration with async SQLAlchemy engine."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import event
from typing import AsyncGenerator
import uuid
from datetime import datetime
import logging

from config import settings

logger = logging.getLogger(__name__)


def _get_pool_kwargs():
    """Build pool configuration based on database type.

    TD-017: SQLite has fundamental write serialization limits.
    For production load, PostgreSQL with proper pool sizing is required.
    """
    # SQLite with aiosqlite doesn't support traditional connection pooling
    # It uses a single file handle, so pool settings are mostly ignored
    if "sqlite" in str(settings.database_url).lower():
        logger.info(
            "SQLite detected - using limited pool config. "
            "For production load, switch to PostgreSQL."
        )
        # SQLite: Use minimal pool to avoid file handle contention
        return {
            "pool_size": 5,
            "max_overflow": 0,  # SQLite doesn't benefit from overflow
            "pool_timeout": settings.db_pool_timeout,
            "pool_recycle": None,  # SQLite doesn't need recycle
            "pool_pre_ping": False,  # SQLite doesn't support pre-ping
        }

    # PostgreSQL: Use full pool configuration
    return {
        "pool_size": settings.db_pool_size,
        "max_overflow": settings.db_max_overflow,
        "pool_timeout": settings.db_pool_timeout,
        "pool_recycle": settings.db_pool_recycle,
        "pool_pre_ping": settings.db_pool_pre_ping,
    }


# Create async engine with proper pool configuration
engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    future=True,
    **_get_pool_kwargs()
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


def generate_uuid() -> str:
    """Generate UUID as string for SQLite compatibility."""
    return str(uuid.uuid4())


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()


# SQLite datetime handling
@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas for foreign key support and other settings."""
    if "sqlite" in str(settings.database_url):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
