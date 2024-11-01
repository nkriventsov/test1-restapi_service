from pydantic_settings import BaseSettings, SettingsConfigDict


# В параметры SettingsConfigDict можно добавить extra="ignore",
# чтобы игнорировать ошибку в случае увеличения переменных окружения в ".env",
# которые не прописаны в здесь
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Формат DSN (data source name)
    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
