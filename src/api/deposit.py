from fastapi import Body, APIRouter

from src.database import async_session_maker, engine
from src.repositories.deposit import DepositRepository

from src.schemas.deposit import DepositRequest


# Создаем маршрутизатор API для обработки запросов на `/deposit`
router = APIRouter(prefix="/deposit", tags=["Депозит"])


# Обработчик POST-запроса для создания депозита
@router.post("")
async def create_deposit(deposit_data: DepositRequest = Body(openapi_examples={
    "1": {
        "summary": "3 месяца",
        "value": {
            "date": "01.01.2024",
            "periods": 3,
            "amount": 100000,
            "rate": 6
        }
    },
    "2": {
        "summary": "9 месяцев",
        "value": {
            "date": "01.01.2024",
            "periods": 9,
            "amount": 100000,
            "rate": 6
        }
    },
    "3": {
        "summary": "12 месяцев",
        "value": {
            "date": "01.01.2024",
            "periods": 12,
            "amount": 100000,
            "rate": 6
        }
    }
})):

    # Открываем сессию для взаимодействия с базой данных через запуск фабрики сессий через контекстный менеджер
    async with async_session_maker() as session:
        # Добавляем данные депозита в БД и сохраняем изменения
        await DepositRepository(session).add_data(deposit_data)
        await session.commit()

    # Возвращаем расчет депозита по месяцам
    return DepositRepository.deposit_dict(deposit_data)
