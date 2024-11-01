from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

# Создаем асинхронный движок для взаимодействия с базой данных, используя URL, указанное в настройках
engine = create_async_engine(settings.DB_URL, echo=True)

# Создаем фабрику асинхронных сессий для работы с БД, где сессии не истекают после коммита
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


# Базовый класс для моделей ORM, на основе которого будут созданы все таблицы базы данных
class Base(DeclarativeBase):
    pass


