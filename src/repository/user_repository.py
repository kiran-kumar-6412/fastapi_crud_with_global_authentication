from src.models.user import User  # Import the correct class
from src.database import local_session
from src.utils import logger
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from sqlalchemy.exc import IntegrityError


class UserRepository:
    @staticmethod
    def create_user(user: dict, db: Session):  # ✅ Pass db directly
        try:
            user_data=user
            user_obj = User(**user_data)  # ✅ Ensure user_data is a dictionary
            print(user_data,"odj -",user_obj)
            db.add(user_obj)
            db.commit()
            db.refresh(user_obj)
            return user_obj
        except Exception as e:
            logger.logging_error(f"Error creating user: {str(e)}")

    @staticmethod
    def user_role(user_role,db:Session):
        db.query(User).filter(User.role==user_role)


    @staticmethod
    def all_users(db:Session):
        try:
            users=db.query(User).all()
            return users
        except Exception as e:
            logger.logging_error(f"getting all users {str(e)}")
    
    @staticmethod
    def Filter_user(id,db:Session):
        user=db.query(User).filter(User.id==id).first()
        return user
    @staticmethod
    def login(username,db:Session):
        user=db.query(User).filter(User.username==username).first()
        return user

    @staticmethod
    def current_user_role(username,db:Session):
        try:
            user=db.query(User).filter(User.username==username).first()
            if user:
                return user.role
        except Exception as e:
            logger.logging_error(f"Current Login User role not found {str(e)}")

    @staticmethod
    def update_user(id,schema_user,db:Session):
        try:
            user_query=db.query(User).filter(User.id==id)
            user=user_query.first()
            print(user)
            if not user:
                print("user not found")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
                
            
            user_query.update(
                {
                "email":schema_user.email,
                "role":schema_user.role
                },synchronize_session=False )
            db.commit()
            db.refresh(user)
            return {"message": "Employee updated successfully", "updated_employee": [f"email={user.email},role={user.role} on username={user.username}"]}
        except IntegrityError as e:
            db.rollback()
            if "Duplicate entry" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists. Please use a different one."
                )
            raise HTTPException(status_code=400, detail="Database integrity error")
        except Exception as e:
            db.rollback()
            logger.logging_error(f"Update User: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))  

    @staticmethod
    def user_delete(id,db:Session):
        user=db.query(User).filter(User.id==id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {id} not found in the database")
        db.query(User).filter(User.id==id).delete(synchronize_session=False)
        db.commit()
        return {"message": f"Employee with ID {id} has been successfully deleted"}
            



            
        