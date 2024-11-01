# Первый этап: Сборка зависимостей и приложения
FROM python:3.12 AS builder

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы Poetry и устанавливаем его
COPY pyproject.toml poetry.lock /app/
RUN python -m pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi  # Устанавливаем все зависимости

# Копируем весь проект в рабочую директорию после установки зависимостей
COPY . /app

# Второй этап: Финальный образ
FROM python:3.12-slim AS final

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и приложение из образа `builder`
COPY --from=builder /app /app

# Добавляем переменные окружения для подключения к базе данных
ENV DB_HOST=$DB_HOST \
    DB_PORT=$DB_PORT \
    DB_USER=$DB_USER \
    DB_PASS=$DB_PASS \
    DB_NAME=$DB_NAME

# Открываем порт для приложения (например, для FastAPI)
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]