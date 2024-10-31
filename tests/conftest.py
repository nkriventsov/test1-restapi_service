import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.config_test import test_settings  # Импорт тестовой конфигурации
from src.schemas.deposit import DepositRequest


# Создание движка и сессии для тестовой базы данных
@pytest.fixture(scope="session")
def async_test_engine():
    """Создает асинхронный движок для тестовой базы данных с параметрами из настроек."""
    return create_async_engine(test_settings.TEST_DB_URL, echo=True)


@pytest.fixture(scope="session", autouse=True)
async def setup_database(async_test_engine):
    """Создает все таблицы в базе данных перед тестами и удаляет после завершения."""
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_session_maker_test(async_test_engine):
    """Фикстура для создания сессий."""
    # Создает фабрику сессий для тестов.
    async_session_factory = sessionmaker(
        bind=async_test_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    # Создает и возвращает сессию для теста, а затем выполняет откат всех изменений.
    async with async_session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
def valid_deposit_data():
    """Возвращает валидный экземпляр данных для `DepositRequest`."""
    return DepositRequest(
        date="01.01.2024",
        periods=3,
        amount=100000,
        rate=6
    )


@pytest.fixture
def invalid_deposit_data():
    """Возвращает невалидный экземпляр данных для `DepositRequest`."""
    return DepositRequest(
        date="32.01.2024",  # Некорректная дата
        periods=61,         # Выходит за диапазон
        amount=5000,        # Меньше допустимого значения
        rate=9              # Выходит за диапазон
    )