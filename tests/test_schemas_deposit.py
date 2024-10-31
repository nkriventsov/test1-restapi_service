import pytest
from src.schemas.deposit import DepositRequest
from pydantic import ValidationError


def test_validate_date():
    """Проверяет валидацию правильного формата даты."""
    deposit_data = DepositRequest(date="01.01.2024", periods=3, amount=100000, rate=5.0)
    assert deposit_data.date == "01.01.2024"


@pytest.mark.parametrize("expected_exception, date, periods, amount, rate",
                         [(ValidationError, "2024/01/01", 3, 100000, 5.0),   # некорректный формат даты
                          (ValidationError, 10, 3, 100000, 5.0),    # некорректный тип данных даты
                          (ValidationError, None, 3, 100000, 5.0),  # пустое значение даты
                          (ValidationError, "01.01.2024", 0, 100000, 5.0),  # значение периода меньше лимита
                          (ValidationError, "01.01.2024", 70, 100000, 5.0),  # значение периода больше лимита
                          (ValidationError, "01.01.2024", "jkj", 100000, 5.0),  # некорректный тип данных периода
                          (ValidationError, "01.01.2024", None, 100000, 5.0),  # пустое значение периода
                          (ValidationError, "01.01.2024", 3, 1000, 5.0),  # значение суммы меньше лимита
                          (ValidationError, "01.01.2024", 3, 5000000, 5.0),  # значение суммы больше лимита
                          (ValidationError, "01.01.2024", 3, "jkj", 5.0),  # некорректный тип данных суммы
                          (ValidationError, "01.01.2024", 3, None, 5.0),  # пустое значение суммы
                          (ValidationError, "01.01.2024", 3, 100000, 0),  # значение процента по вкладу меньше лимита
                          (ValidationError, "01.01.2024", 3, 100000, 10),  # значение процента по вкладу больше лимита
                          (ValidationError, "01.01.2024", 3, 100000, "jkj"),  # некорректный тип данных процента по вкл.
                          (ValidationError, "01.01.2024", 3, 100000, None),  # пустое значение процента по вкладу
                          ])
def test_invalid_date(expected_exception, date, periods, amount, rate):
    """Проверяет, что несоответствующие формат или значение входных данных вызывают ошибку валидации."""
    with pytest.raises(expected_exception):
        DepositRequest(date=date, periods=periods, amount=amount, rate=rate)
