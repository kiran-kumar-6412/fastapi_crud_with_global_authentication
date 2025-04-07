from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM:str = os.getenv("ALGORITHM")
    EXPIRE_TIME_MINUTES:int = os.getenv("EXPIRE_TIME_MINUTES")

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")