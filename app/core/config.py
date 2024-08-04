from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    DB_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
