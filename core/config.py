from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    weather_api_key: str | None = 'b1b15e88fa797225412429c1c50c122a1'

    log_level: str = "INFO"
    log_renderer: str = "console"  # console | json

    class Config:
        env_file = ".env"


settings = Settings()
