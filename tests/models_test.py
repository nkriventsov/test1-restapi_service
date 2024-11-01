from sqlalchemy.orm import Mapped, mapped_column
from tests.database_test import BaseTest


# Модель ORM для таблицы депозитов
class DepositOrmTest(BaseTest):
    __tablename__ = "deposits"  # Имя таблицы в базе данных

    id: Mapped[int] = mapped_column(primary_key=True)  # Первичный ключ
    date: Mapped[str] = mapped_column(nullable=False)  # Дата вклада
    periods: Mapped[int] = mapped_column(nullable=False)  # Количество месяцев по вкладу
    amount: Mapped[int] = mapped_column(nullable=False)  # Сумма вклада
    rate: Mapped[float] = mapped_column(nullable=False)  # Процентная ставка

