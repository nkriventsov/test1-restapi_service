import pytest
from src.repositories.deposit import DepositRepository
from src.schemas.deposit import DepositRequest


@pytest.mark.asyncio
async def test_deposit_repository(async_session_maker_test):
    """Проверяет репозиторий на корректное добавление и расчет депозита."""
    repo = DepositRepository(async_session_maker_test)
    deposit_data = DepositRequest(date="01.01.2024", periods=3, amount=100000, rate=5.0)

    # Добавляет данные в базу
    result = await repo.add_data(deposit_data)
    assert result.date == deposit_data.date
    assert result.periods == deposit_data.periods
    assert result.amount == deposit_data.amount
    assert result.rate == deposit_data.rate

    # Проверяет расчет доходности депозита
    deposit_calculations = repo.deposit_dict(deposit_data)
    assert "31.01.2024" in deposit_calculations
    assert deposit_calculations == {'31.01.2024': 100416.67, '29.02.2024': 100835.07, '31.03.2024': 101255.22}
