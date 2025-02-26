import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


def _getenv(name: str, default: str = None) -> str | None:
    value = os.getenv(name, default)
    return value


class Configs(BaseSettings):

    DB_ENGINE: str = _getenv("DB_ENGINE")
    DB_USER: str = _getenv("DB_USER")
    DB_PASSWORD: str = _getenv("DB_PASSWORD")
    DB_HOST: str = _getenv("DB_HOST")
    DB_PORT: str = _getenv("DB_PORT")
    DATA_BASE: str = _getenv("DATA_BASE")

    DATABASE_URI: str = (
        "{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
            db_engine=DB_ENGINE,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DATA_BASE,
        )
    )


configs = Configs()
