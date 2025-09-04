from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    weather_api_key: str | None = Field(validation_alias="WEATHER_API")
    openai_api_key: str | None = Field(validation_alias="OPENAI_API_KEY")

    log_level: str = "INFO"
    log_renderer: str = "console"  # console | json

    model_gpt: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"


settings = Settings()
