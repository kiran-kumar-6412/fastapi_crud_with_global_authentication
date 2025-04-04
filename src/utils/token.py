import jwt
from datetime import timedelta,datetime
from src.config.config import settings
from src.utils import logger
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
from fastapi import HTTPException,status
from src.schemas.user import TokenData


SECRETE_KEY=settings.SECRET_KEY
EXPIRE_TIME_MINUTES=settings.EXPIRE_TIME_MINUTES
ALGORITHM=settings.ALGORITHM

def create_token(data:dict):
    try:
        to_encode=data.copy()
        expire=datetime.utcnow()+timedelta(EXPIRE_TIME_MINUTES)
        to_encode.update({'exp':expire})
        access_token=jwt.encode(to_encode,SECRETE_KEY,algorithm=ALGORITHM)
        return (access_token)
    except Exception as e:
        logger.logging_error(f"Token Create Error {str(e)}")


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        return username  # Successfully authenticated

    except ExpiredSignatureError:
        logger.logging_error("Token Expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Session Expired, please log in again"
        )

    except InvalidTokenError:
        logger.logging_error("Invalid Token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )