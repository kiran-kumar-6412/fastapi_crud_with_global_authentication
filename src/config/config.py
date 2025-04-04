from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:kiran%40123@localhost/fastapi?charset=utf8mb4"
    REDIS_HOST: str = "localhost"
    SECRET_KEY: str = "kiran123"
    REDIS_PORT: int = 6479  
    ALGORITHM:str = 'HS256'
    EXPIRE_TIME_MINUTES:int = 30

    class Config:
        env_file = ".env"  # ✅ Pydantic loads .env automatically

# Create a settings instance
settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")