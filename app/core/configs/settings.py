from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    key_path: str
    cred: str
    ts_cl: str
    ts_stuff: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    return Settings()