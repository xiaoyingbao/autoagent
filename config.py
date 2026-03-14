from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/autoagent"
    redis_url: str = "redis://localhost:6379"
    model_name: str = "gpt-4o-mini"
    max_tokens: int = 1500
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()



