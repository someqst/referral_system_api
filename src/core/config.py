from typing import Literal
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_PATH = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    DB_URI: SecretStr
    LOGGING_LEVEL: Literal["DEBUG", "INFO", "ERROR", "WARNING", "CRITICAL"] = "DEBUG"
    ALGORITHM: SecretStr
    SECRET_KEY: SecretStr

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / ".env", enable_decoding="utf-8"
    )


settings = Settings()


def get_auth_data():
    return {
        "algorithm": settings.ALGORITHM.get_secret_value(),
        "secret_key": settings.SECRET_KEY.get_secret_value(),
    }
