from typing import Callable, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine as _create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from bot.config import DatabaseSettings

Base = declarative_base()


def create_async_engine(db_settings: DatabaseSettings):
    """
    Создает асинхронный движок базы данных
    """
    return _create_async_engine(
        db_settings.url,
        echo=False,
        pool_pre_ping=True
    )


def get_session_maker(engine) -> async_sessionmaker:
    """
    Создает фабрику сессий базы данных
    """
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session(session_maker: Callable[[], AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор сессий для контекстного менеджера
    """
    session = session_maker()
    try:
        yield session
    finally:
        await session.close()
