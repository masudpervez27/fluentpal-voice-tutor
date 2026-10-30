from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "FluentPal Voice Tutor API"
    frontend_origin: str = "http://localhost:5173"
    log_level: str = "INFO"


settings = Settings()
