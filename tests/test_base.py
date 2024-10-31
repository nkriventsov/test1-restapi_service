import pytest
from src.repositories.base import BaseRepository
from src.models.deposit import DepositOrm

@pytest.mark.asyncio
async def test_add_data(async_session_maker_test, valid_deposit_data):
    """Тестирует добавление данных в базу через `BaseRepository`."""
    async with async_session_maker_test() as session:
        repo = BaseRepository(session)
        repo.model = DepositOrm
        repo.schema = valid_deposit_data.__class__
        result = await repo.add_data(valid_deposit_data)
        assert result.date == valid_deposit_data.date
        assert result.amount == valid_deposit_data.amount
