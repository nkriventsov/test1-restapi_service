import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import async_session_maker


@pytest.mark.asyncio
async def test_database_session():
    """Тестирует создание асинхронной сессии для подключения к базе данных."""
    async with async_session_maker() as session:
        # проверяем, что созданный объект `session` является экземпляром `AsyncSession`.
        assert isinstance(session, AsyncSession)