import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from tests.database_test import BaseTest
from tests.config_test import test_settings  # Импорт тестовой конфигурации
from src.schemas.deposit import DepositRequest
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """Создает event loop для всех тестов с областью session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Создание движка и сессии для тестовой базы данных
@pytest.fixture(scope="session")
def async_test_engine():
    """Создает асинхронный движок для тестовой базы данных с параметрами из настроек."""
    return create_async_engine(test_settings.TEST_DB_URL)


@pytest.fixture(scope="session", autouse=True)
async def setup_database(async_test_engine):
    """Создает все таблицы в базе данных перед тестами и удаляет после завершения."""
    async with async_test_engine.begin() as conn:   # открывает подключение к базе данных для выполнения команд
        # создает все таблицы базы данных, используя метаданные, определенные в `Base`
        await conn.run_sync(BaseTest.metadata.create_all)
    yield   # позволяет выполнить тесты между созданием и удалением таблиц
    async with async_test_engine.begin() as conn:
        # удаляет все таблицы после завершения тестов
        await conn.run_sync(BaseTest.metadata.drop_all)


@pytest.fixture
async def async_session_maker_test(async_test_engine):
    """Фикстура для создания сессий."""
    # Создает фабрику сессий для тестов.
    async_session_factory = sessionmaker(
        bind=async_test_engine, # привязывает сессии к указанному движку(async_test_engine)
        expire_on_commit=False, # объекты, загруженные из сессии, сохраняют свои данные после команды commit
        class_=AsyncSession # предоставляет возможность выполнения асинхронных операций с базой данных
    )
    # Создает и возвращает сессию для теста, а затем выполняет откат всех изменений.
    async with async_session_factory() as session:
        # передает созданную сессию в тест
        yield session
        # выполняет откат всех изменений после завершения теста
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
