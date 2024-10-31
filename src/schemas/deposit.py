from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime


# Схема данных для запроса на создание депозита
class DepositRequest(BaseModel):
    date: str  # Дата в формате строки
    periods: int = Field(ge=1, le=60)  # Количество месяцев вклада, от 1 до 60
    amount: int = Field(ge=10000, le=3000000)  # Сумма вклада от 10 000 до 3 000 000
    rate: float = Field(ge=1, le=8)  # Процентная ставка, от 1 до 8

    # Валидатор для поля `date`, проверяющий соответствие формату
    @field_validator('date')
    @classmethod
    def validate_date(cls, date):
        try:
            datetime.strptime(date, "%d.%m.%Y")
            return date
        except ValueError:
            raise ValueError('Введите дату в корректном формате:  dd.mm.YYYY')

    # Включаем опцию, чтобы позволить использовать атрибуты ORM в pydantic-схемах
    model_config = ConfigDict(from_attributes=True)
