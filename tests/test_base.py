import pytest
from src.repositories.base import BaseRepository
from src.models.deposit import DepositOrm

@pytest.mark.asyncio
async def test_add_data(async_session_maker_test, valid_deposit_data):
    """Тестирует добавление данных в базу через `BaseRepository`."""
    session = async_session_maker_test  # Используем сессию напрямую

    # Создаем экземпляр BaseRepository,
    # передавая ему объект сессии session для управления операциями с базой данных.
    repo = BaseRepository(session)

    # Задаем модель репозитория BaseRepository как DepositOrm, чтобы указать,
    # с какой таблицей в базе данных будем работать.
    repo.model = DepositOrm

    # Устанавливаем схему репозитория как класс фикстуры valid_deposit_data,
    # тем самым определяя, какую схему данных репозиторий будет использовать для проверки и приведения данных.
    repo.schema = valid_deposit_data.__class__

    # Асинхронно вызываем метод add_data репозитория,
    # передавая валидные данные депозита valid_deposit_data.
    # Возвращенное значение (запись в базе данных) сохраняем в переменной result
    result = await repo.add_data(valid_deposit_data)

    # Проверяем, что значение date в результате совпадает с date из переданных данных,
    # подтверждая корректность сохранения данных.
    assert result.date == valid_deposit_data.date

    # Проверяем, что значение periods в результате совпадает с periods из переданных данных.
    assert result.periods == valid_deposit_data.periods

    # Проверяем, что значение amount в результате совпадает с amount из переданных данных.
    assert result.amount == valid_deposit_data.amount

    # Проверяем, что значение rate в результате совпадает с rate из переданных данных.
    assert result.rate == valid_deposit_data.rate
