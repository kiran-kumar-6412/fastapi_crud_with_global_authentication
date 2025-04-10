from src.repository.user_repository import UserRepository
from src.utils.security import hash_password,logger,verify_password
from src.utils.token import create_token,verify_token
from fastapi import HTTPException,status,Depends
from src.schemas.user import TokenData




def user_create(user, db):
    try:
        user_data = user.dict()  # ✅ Convert Pydantic model to dictionary
        user_data["password"] = hash_password(user_data["password"])  # ✅ Modify password securely
        return UserRepository.create_user(user_data, db)  # ✅ Pass dictionary

    except Exception as e:
        logger.logging_error(f"USer Create Error {str(e)}")

def get_all_users(db):

    return UserRepository.all_users(db)

def filter_user(id:int,db):
    return UserRepository.Filter_user(id,db)

def login(user,db):
    try:
        # print(user,user.username,user.password)
        username=user.username
        password=user.password
        user_record=UserRepository.login(username,db)

        if not username or not verify_password(password,user_record.password):
            raise HTTPException(status.HTTP_404_NOT_FOUND,"Invalid Credentials")
        if not user_record.is_active:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User is not active")

        access_token = create_token({"sub": user_record.username, "role": user_record.role})
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.logging_error(f"loggin error {str(e)}")


def current_user(token_data: TokenData = Depends(verify_token)):
    #print("token getting to current user",token_data)
    try:
        return token_data.username
    except Exception as e:
        logger.logging_error(f"Current User Error {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    


def update_user(id,schema_user,session_username,db):
    login_user_role=UserRepository.current_user_role(session_username,db)
    if login_user_role=="admin":               # only admin can update the user details
       return UserRepository.update_user(id,schema_user,db)
    return {"message":"You Are not Autherise to update user"}

def user_delete(id,session_username,db):
    login_user_role=UserRepository.current_user_role(session_username,db)
    if login_user_role=="admin":               # only admin can update the user details
        return UserRepository.user_delete(id,db)
    return {"message":"You Are not Autherise to update user"}


def create_or_update_user(id,data,session_user,db):
    if id <= 0 and data.create_data:
        user=user_create(data.create_data, db)
        if not user:
            raise HTTPException(status_code=400, detail="User creation failed")
        return user
    elif data.update_data:
        return update_user(id, data.update_data, session_user, db)
    else:
        raise HTTPException(status_code=400, detail="Invalid input for create/update.")

