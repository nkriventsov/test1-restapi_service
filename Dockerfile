# Базовый образ с Python
FROM python:3.12-slim

# Установка curl для установки Poetry
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get remove -y curl && rm -rf /var/lib/apt/lists/*

# Добавление Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы для Poetry
COPY pyproject.toml poetry.lock /app/

# Отключаем виртуальные окружения, чтобы Poetry установил зависимости в системное окружение
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем остальные файлы проекта
COPY . /app

# Проверяем установку alembic
RUN alembic --version

# Открываем порт для приложения
EXPOSE 8000

# Запуск приложения через Poetry
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
