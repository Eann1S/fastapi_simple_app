from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_url: str
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
