from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATA_PLATFORM_BASE_URL: str = "http://localhost:80"

settings = Settings()
