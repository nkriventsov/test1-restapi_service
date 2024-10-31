from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root_endpoint():
    """Проверяет, что базовый эндпоинт работает и возвращает код 404 (Not Found)."""
    # отправляет GET-запрос на корневой эндпоинт (`/`) приложения.
    response = client.get("/")
    # проверяет, что сервер возвращает статус 404, так как корневой эндпоинт не определен.
    assert response.status_code == 404
