from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    load_dotenv()
    key_path: str = os.getenv('KEY_PATH')

  
def get_settings():
    return Settings()