import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("Нет токена в .env файле!")


class Settings(BaseSettings):
    DATABASE_URL: str
    BOT_TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()
