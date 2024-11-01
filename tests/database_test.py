from sqlalchemy.orm import DeclarativeBase


# Базовый класс для моделей ORM, на основе которого будут созданы все таблицы базы данных
class BaseTest(DeclarativeBase):
    pass


