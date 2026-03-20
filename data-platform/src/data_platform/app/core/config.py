from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SPARK_CONNECT_URL: str = "sc://localhost:15002"

settings = Settings()
