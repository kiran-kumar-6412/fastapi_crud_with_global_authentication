from src.repository.user_repository import UserRepository
from src.utils.security import hash_password, logger, verify_password
from src.utils.token import create_token, verify_token
from fastapi import HTTPException, status, Depends
from src.schemas.user import TokenData, UserListResponse, ShowUser
from sqlalchemy.orm import Session


def user_create(user, db):
    try:
        user_data = user.dict()  # ✅ Convert Pydantic model to dictionary
        user_data["password"] = hash_password(user_data["password"])  # ✅ Modify password securely
        user = UserRepository.create_user(user_data, db)  # ✅ Pass dictionary
        if user:
            return {"data": user,
                    "status": True,
                    "message": "User Created Successfully "}
        return {
            "data": None,
            "status": False,
            "message": "User Creation Failed!"
        }

    except Exception as e:
        logger.logging_error(f"User Create Error {str(e)}")

def get_all_users(db: Session):
    try:
        users = UserRepository.all_users(db)
        if users:
            return {"data": users,
            "status": True,
            "message":"User Found"}
        else:
            # If no users are found, return an appropriate response
            return {
                        "data": None,
                        "status": False,
                        "message": "No users found"
                    }
    except Exception as e:
            # Log any errors that occur during the process
            logger.logging_error(f"Error fetching all users: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
                


def filter_user(id:int,db):
    user= UserRepository.Filter_user(id,db)
    if user:
        return {"data": user,
            "status": True,
            "message":"User Found"}
    
    return {
                "data": None,
                "status": False,
                "message": "User is not Found"
            }

def login(user, db):
    try:
        username = user.username
        password = user.password

        user_record = UserRepository.login(username, db)
        if not user_record:
            return {
                "data": None,
                "status": False,
                "message": "User not found"
            }

        if not verify_password(password, user_record.password):
            return {
                "data": None,
                "status": False,
                "message": "Invalid credentials"
            }

        if not user_record.is_active:
            return {
                "data": None,
                "status": False,
                "message": "User is not active"
            }

        access_token = create_token({"sub": user_record.username, "role": user_record.role},db)

        return {
            "data": {
                "access_token": access_token,
                "token_type": "bearer"
            },
            "status": True,
            "message": "Login successful"
        }

    except Exception as e:
        logger.logging_error(f"Login error: {str(e)}")
        return {
            "data": None,
            "status": False,
            "message": "Internal Server Error"
        }


def current_user(token_data: TokenData = Depends(verify_token)):
    #print("token getting to current user",token_data)
    try:
        user= token_data.username
        if user:
            return {"data": user,
                "status": True,
                "message":"User details sucessfully Fetched"}
        return {
                "data": None,
                "status": False,
                "message": "Users not found something went wrong"
            }
    except Exception as e:
        logger.logging_error(f"Current User Error {str(e)}")
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Invalid authentication credentials"
        # )
    


def update_user(id,schema_user,session_username,db):
    login_user_role=UserRepository.current_user_role(session_username,db)
    if login_user_role=="admin":               # only admin can update the user details
       return UserRepository.update_user(id,schema_user,db)
    return {
                "data": None,
                "status": False,
                "message": "You are not authorized to update this user"
            }
    # raise HTTPException(status_code=403, detail="You are not authorized to update this user")

def user_delete(id,session_username,db):
    login_user_role=UserRepository.current_user_role(session_username,db)
    if login_user_role=="admin":               # only admin can update the user details
        user= UserRepository.user_delete(id,db)
        if user:
            return {"data": user,
                "status": True,
                "message":"User deleted Sucessfully"}
        return {
                "data": None,
                "status": False,
                "message": "something went wrong"
            }
    return {    
                "data": None,
                "status": False,
                "message": "You are not authorized to delete this user"
            }
    #raise HTTPException(status_code=403, detail="You are not authorized to delete this user")



def create_or_update_user(id,data,session_user,db):
    if id <= 0 and data.create_data:
        user=user_create(data.create_data, db)
        if not user:
            return {    
                "data": None,
                "status": False,
                "message": "User creation failed"
            }
            #raise HTTPException(status_code=400, detail="User creation failed")
        return {    
                "data": user,
                "status": True,
                "message": "User created Sucessfully!"
            }
    elif data.update_data:
        return update_user(id, data.update_data, session_user, db)
    else:
        return {    
                "data": None,
                "status": False,
                "message": "Invalid input for create/update."
            }
        #raise HTTPException(status_code=400, detail="Invalid input for create/update.")

