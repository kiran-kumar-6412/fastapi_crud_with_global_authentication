from src.repository.user_repository import UserRepository
from src.utils.security import hash_password, logger, verify_password
from src.utils.token import create_token, verify_token
from fastapi import HTTPException, status, Depends
from src.schemas.user import TokenData, UserListResponse, ShowUser
from sqlalchemy.orm import Session
import json

def user_create(user, db):
    try:
        user_data = user.dict()

        # Check username/email uniqueness
        verify = UserRepository.check_username_or_email(user_data["username"], user_data["email"], db)
        if verify["username_exists"]:
            return {
                "data": None,
                "status": False,
                "message": "Username already taken"
            }
        elif verify["email_exists"]:
            return {
                "data": None,
                "status": False,
                "message": "Email id already associated with another account"
            }

        # Hash password
        user_data["password"] = hash_password(user_data["password"])

        # Create user
        created_user = UserRepository.create_user(user_data, db)

        if created_user:
            user_dict = {
                "id": created_user.id,
                "username": created_user.username,
                "email": created_user.email,
                "role": created_user.role
            }
            return {
                "data": json.dumps(user_dict),
                "status": True,
                "message": "User created successfully!"
            }

        return {
            "data": None,
            "status": False,
            "message": "User creation failed"
        }
    except Exception as e:
        logger.logging_error(f"User Create Error {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error{str(e)}")


def get_all_users(db: Session):
    try:
        users = UserRepository.all_users(db)
        if users:
            # Convert each User object to a dictionary manually
            users_list = [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
                for user in users
            ]
            return {"data": json.dumps(users_list),
            "status": True,
            "message":"All users details"}
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
            raise HTTPException(status_code=500, detail=f"Internal Server Error {str(e)}")
                


def filter_user(id:int,db):
    user= UserRepository.Filter_user(id,db)
    if user:
        user_list = [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
                for user in user
            ]
        return {"data": json.dumps(user_list),
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

        access_token = create_token({"sub": user_record.username, "role": user_record.role})
        return {
                
                "access_token": access_token,
                "token_type": "bearer"
                         ,
            "status": True,
            "message": "Login successful"
        }

    except Exception as e:
        logger.logging_error(f"Login error: {str(e)}")
        return {
            "data": None,
            "status": False,
            "message": f"Internal Server Error{str(e)}"
        }


def current_user(token_data: TokenData = Depends(verify_token)):
    try:
        username= token_data.username
        if username:
            return username
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
       user= UserRepository.update_user(id,schema_user,db)

       if not user:
            return {
                "data": None,
                "status": False,
                "message": f"User with ID {id} not found"
            }
       elif user.email:
            return {
                "data": None,
                "status": False,
                "message": f"Email id Already associated with another account"
                }
       
       users_list = [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }]
       return {    
                "data": json.dumps(users_list),
                "status": True,
                "message": "user updated successfully:"
            }

    return {
                "data": None,
                "status": False,
                "message": f"You are not authorized to update this user your role was {login_user_role}"
            }
    # raise HTTPException(status_code=403, detail="You are not authorized to update this user")

def user_delete(id,session_username,db):
    login_user_role=UserRepository.current_user_role(session_username,db)
    if login_user_role=="admin":               # only admin can update the user details
        return UserRepository.user_delete(id,db)
       
    
    return {    
                "data": None,
                "status": False,
                "message": "You are not authorized to delete this user"
            }
    #raise HTTPException(status_code=403, detail="You are not authorized to delete this user")



def create_or_update_user(id,data,session_user,db):
    if id <= 0 and data.create_data:
        return user_create(data.create_data, db)
       
            #raise HTTPException(status_code=400, detail="User creation failed")
        
    elif data.update_data:
        print("seesionuse",session_user)
        return update_user(id, data.update_data, session_user, db)
    else:
        return {    
                "data": None,
                "status": False,
                "message": "Invalid input for create/update."
            }
        #raise HTTPException(status_code=400, detail="Invalid input for create/update.")

