from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):

    MODE: Literal["DEV", "TEST", "PROD"]

    DB_URL: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    TEST_DB_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
