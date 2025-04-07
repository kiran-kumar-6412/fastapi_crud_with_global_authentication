from fastapi import APIRouter, Depends,HTTPException,status
from src.schemas.user import UserCreate, UserBase,ShowUser,Login,User_update
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.services import user_services
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.post("/register",response_model=ShowUser)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return user_services.user_create(user, db)


@router.post("/login")
def login(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    return user_services.login(user,db)

@router.get("/all",response_model=list[ShowUser])
def get_user(username: str = Depends(user_services.current_user),db: Session = Depends(get_db)):  
    return user_services.get_all_users(db)

@router.get("/{id}",response_model=ShowUser)
def filter_user(id:int,db:Session=Depends(get_db),username: str = Depends(user_services.current_user)):
    user=user_services.filter_user(id,db)
    if user:
        return user
    raise HTTPException(status.HTTP_404_NOT_FOUND,f"user with id-{id} not found")

@router.put("/{id}")
def update_user(id:int,schema_user:User_update,session_username:str=Depends(user_services.current_user),db:Session=Depends(get_db)):
    return user_services.update_user(id,schema_user,session_username,db)

@router.delete("/id")
def user_delete(id:int,session_username:str=Depends(user_services.current_user),db:Session=Depends(get_db)):
    return user_services.user_delete(id,session_username,db)