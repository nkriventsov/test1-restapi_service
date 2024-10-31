from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

# Добавляем родительскую директорию в путь, чтобы иметь доступ к модулям в `src`
sys.path.append(str(Path(__file__).parent.parent))

# Импортируем роутер для депозитов
from src.api.deposit import router as router_deposit

# Создаем экземпляр FastAPI
app = FastAPI()

# Подключаем роутер депозитов к приложению
app.include_router(router_deposit)


if __name__ == '__main__':
    # Основной блок запуска для запуска приложения с помощью Uvicorn в режиме перезагрузки
    # Вариант без worker'ов
    uvicorn.run(
                "main:app",
                reload=True
                )
#
#     # Вариант c worker'ами
#     uvicorn.run(
#                 "main:app",
#                 reload=True,
#                 workers=5
#                 )

