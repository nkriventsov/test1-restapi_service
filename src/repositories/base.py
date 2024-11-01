from pydantic import BaseModel
from sqlalchemy import insert


# Базовый репозиторий для работы с моделью в БД
class BaseRepository:
    model = None  # Модель базы данных, с которой работает репозиторий
    schema: BaseModel = None  # Pydantic-схема, используемая для валидации данных

    # Инициализируем репозиторий, передавая сессию для работы с БД извне
    def __init__(self, session):
        self.session = session

    # Асинхронный метод для добавления данных в БД
    async def add_data(self, data: BaseModel):

        # Создаем SQL-запрос на вставку данных в модель
        add_data_stmt = (insert(self.model)
                         .values(**data.model_dump())
                         .returning(self.model))

        # Выполняем запрос в базе данных и получаем результат
        result = await self.session.execute(add_data_stmt)

        # Извлекаем один объект из результатов запроса
        model = result.scalars().one()

        # Преобразуем ORM-объект в pydantic-схему и возвращаем его
        return self.schema.model_validate(model)






