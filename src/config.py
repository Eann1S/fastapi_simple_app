from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    postgres_url: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_exp_millis: int
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
