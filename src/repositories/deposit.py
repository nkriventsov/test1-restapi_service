from src.repositories.base import BaseRepository
from src.models.deposit import DepositOrm
from src.schemas.deposit import DepositRequest
from pydantic import BaseModel

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Описание формулы ежемесячной капитализации
'''
Ежемесячная капитализация

Формула расчёта дохода по депозиту с ежемесячной капитализацией:
Д = Р * (1 + N/12)^T
Д — итоговый доход, то есть размер вклада на конец срока включая сумму открытия и начисленный процент,
P — начальный депозит,
N — годовая ставка, разделенная на 100,
T — срок договора в месяцах. 
'''


class DepositRepository(BaseRepository):
    model = DepositOrm  # Модель базы данных для работы с депозитами
    schema = DepositRequest  # Схема pydantic для валидации данных

    # Статический метод для конвертации строки даты в объект `datetime`
    @staticmethod
    def date_convert(date_str):
        return datetime.strptime(date_str, "%d.%m.%Y")

    # Метод для вычисления конечной даты после добавления `months` месяцев к `date_str`
    @staticmethod
    def final_date(date_str, months):
        date = DepositRepository.date_convert(date_str) - timedelta(days=1)
        return (date + relativedelta(months=months)).strftime("%d.%m.%Y")

    # Метод для вычисления итоговой суммы депозита с капитализацией
    @staticmethod
    def deposit_calc(amount, rate, months):
        return round(amount * (1 + (rate/100)/12)**months, 2)

    # Метод для создания словаря с ежемесячными расчетами депозита
    @staticmethod
    def deposit_dict(data: BaseModel):

        result = {}

        for month in range(1, data.periods + 1):
            result[DepositRepository.final_date(data.date, month)] = (DepositRepository.deposit_calc(data.amount,
                                                                                                     data.rate,
                                                                                                     month))

        return result
