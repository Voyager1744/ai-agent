from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    weather_api_key: str | None = Field(validation_alias="WEATHER_API")

    log_level: str = "INFO"
    log_renderer: str = "console"  # console | json

    class Config:
        env_file = ".env"


settings = Settings()
