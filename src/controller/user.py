from fastapi import APIRouter, Depends,HTTPException,status,Body
from src.schemas.user import UserCreate, UserBase,ShowUser,Login,User_update,UserActionSchema,MessageResponse
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.services import user_services
from fastapi.security import OAuth2PasswordRequestForm
from typing import Union


router = APIRouter()

# @router.post("/register",response_model=ShowUser)
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     return user_services.user_create(user, db)


@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)): # getting form_data from swagger ui
    return user_services.login(form_data,db)

@router.get("/all",response_model=list[ShowUser])
def get_user(current_user : str = Depends(user_services.current_user),db: Session = Depends(get_db)):  
    return user_services.get_all_users(db)

@router.post("/user-action/{id}",response_model=Union[ShowUser,MessageResponse])
def create_or_update_user(id:int,data:UserActionSchema,session_user:str=Depends(user_services.current_user),db:Session=Depends(get_db)):
    #print("Current User:", session_user)
    return user_services.create_or_update_user(id,data,session_user,db)



# @router.get("/{id}",response_model=ShowUser)
# def filter_user(id:int,db:Session=Depends(get_db),username: str = Depends(user_services.current_user)):
#     user=user_services.filter_user(id,db)
#     if user:
#         return user
#     raise HTTPException(status.HTTP_404_NOT_FOUND,f"user with id-{id} not found")

# @router.put("/update/{id}")
# def update_user(id:int,schema_user:User_update,session_username:str=Depends(user_services.current_user),db:Session=Depends(get_db)):
#     return user_services.update_user(id,schema_user,session_username,db)

@router.delete("/id")
def user_delete(id:int,session_username:str=Depends(user_services.current_user),db:Session=Depends(get_db)):
    return user_services.user_delete(id,session_username,db)