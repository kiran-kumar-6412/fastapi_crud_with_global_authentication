from src.config.config import Oauth2_schema
from src.utils.token import verify_token
from fastapi import Depends




def current_user(token:str=Depends(Oauth2_schema)):
    pass


