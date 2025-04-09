from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_TIME_MINUTES: int

    class Config:
        env_file = ".env"  # 👈 Pydantic will load variables from this

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
