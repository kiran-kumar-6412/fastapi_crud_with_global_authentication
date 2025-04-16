from src.models.user import User  # Import the correct class
from src.database import local_session
from src.utils import logger
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from src.schemas.user import MessageResponse

class UserRepository:
    @staticmethod
    def check_username_or_email(username:str ,email ,db: Session):
        try:
            result=db.execute(text("SELECT username FROM users WHERE username=:username"),{"username":username})
            username_result=result.first()
            result=db.execute(text("SELECT email FROM users WHERE email=:email"),{"email":email})
            email_result=result.first()
            return {
            "username_exists": username_result ,
            "email_exists": email_result 
        }

        except Exception as e:
            logger.logging_error(f"username or email validation error{str(e)}")

    @staticmethod
    def create_user(user: dict, db: Session):  # ✅ Pass db directly
        try:
            user_data=user
            user_obj = User(**user_data)  # ✅ Ensure user_data is a dictionary
            #print(user_data,"odj -",user_obj)
            db.add(user_obj)
            db.commit()
            db.refresh(user_obj)
            print("user oject",user_obj)
            return user_obj
        
        except Exception as e:
            logger.logging_error(f"Error creating user: {str(e)}")
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,detail=f"error in use creation {str(e)}")

    # @staticmethod
    # def user_role(user_role,db:Session):
    #     sql=text("SELECT * from users WHERE role=:role")
    #     result=db.execute(sql,{"role":user_role})
    #     db.query(User).filter(User.role==user_role)


    @staticmethod
    def all_users(db: Session):
        try:
            sql = text("SELECT * FROM users")
            result = db.execute(sql)
            users = result.fetchall()           
            users= [User(**row._mapping) for row in users]           
            return users
        except Exception as e:
            logger.logging_error(f"Error getting all users: {str(e)}")
            # raise HTTPException(status_code=500, detail="Failed to fetch users")
    
    @staticmethod
    def Filter_user(id,db:Session):
        result=db.execute(text("SELECT * FROM users WHERE id=:id"),{"id":id})
        user=result.first()
        return [User(**user._mapping) if user else None]
    
    @staticmethod
    def login(username, db: Session):
        try:
            sql = text("SELECT * FROM users WHERE username = :username")
            result = db.execute(sql, {"username": username})
            row = result.fetchone()

            if row:
                return User(**row._mapping)  # Convert row to ORM User object
            return None
        except Exception as e:
            logger.logging_error(f"Error logging in: {str(e)}")
            #raise HTTPException(status_code=500, detail="Failed to fetch login user")

    @staticmethod
    def current_user_role(username, db: Session):       
        try:
            sql = text("SELECT * FROM users WHERE username = :username")
            result = db.execute(sql, {"username": username}).fetchone()
            user = User(**result._mapping)
            print("your role",user.role,"userdetails",user)
            return user.role
        

        except Exception as e:
            logger.logging_error(f"Current Login User role not found {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to get user role {str(e)}")

    @staticmethod
    def update_user(id,schema_user,db:Session):
        try:
            result=db.execute(text("SELECT * FROM users WHERE id=:id"),{"id":id})
            user=result.fetchone()
            if not user:
               return None
                #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
            result=db.execute(text("SELECT * FROM users WHERE email=:email"),{"email":schema_user.email})
            email=result.fetchone() 
            if email:
               return email

            sql_update=text("UPDATE users SET email=:email,role=:role WHERE id=:id")
            db.execute(sql_update,{"email":schema_user.email,"role":schema_user.role,"id":id})
            db.commit()

            updated_sql = text("SELECT * FROM users WHERE id = :id")
            updated_result = db.execute(updated_sql, {"id": id}).first()
            user = User(**updated_result._mapping)
            return user
        except IntegrityError as e:
            db.rollback()
            if "Duplicate entry" in str(e.orig):
                return {
                        "data": None,
                        "status": False,
                        "message": "Email already exists. Please use a different one."
                        }
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail="Email already exists. Please use a different one."
            #     )
            # raise HTTPException(status_code=400, detail="Database integrity error")
        except Exception as e:
            db.rollback()
            logger.logging_error(f"Update User: {str(e)}")
            #raise HTTPException(status_code=500, detail=str(e))  

    @staticmethod
    def user_delete(id,db:Session):
        try:
            result=db.execute(text("SELECT * FROM users WHERE id=:id"),{"id":id})        
            user=result.first()
            if not user:
                return {
                        "data": None,
                        "status": False,
                        "message": f"Employee with ID {id} not found in the database"
                        }
                #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {id} not found in the database")
            sql_quary=text("DELETE FROM users WHERE id=:id")
            db.execute(sql_quary,{"id":id})
            db.commit()
            return {"data":True,"status":True,"message": f"Employee with ID {id} has been successfully deleted"}
        except Exception as e:
            db.rollback()
            logger.logging_error(f"Delete User: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to delete user")
                












#  orm




# class UserRepository:
#     @staticmethod
#     def create_user(user: dict, db: Session):  # ✅ Pass db directly
#         try:
#             user_data=user
#             user_obj = User(**user_data)  # ✅ Ensure user_data is a dictionary
#             print(user_data,"odj -",user_obj)
#             db.add(user_obj)
#             db.commit()
#             db.refresh(user_obj)
#             return user_obj
#         except Exception as e:
#             logger.logging_error(f"Error creating user: {str(e)}")

#     @staticmethod
#     def user_role(user_role,db:Session):
#         db.query(User).filter(User.role==user_role)


#     @staticmethod
#     def all_users(db:Session):
#         try:
#             users=db.query(User).all()
#             return users
#         except Exception as e:
#             logger.logging_error(f"getting all users {str(e)}")
    
#     @staticmethod
#     def Filter_user(id,db:Session):
#         user=db.query(User).filter(User.id==id).first()
#         return user
#     @staticmethod
#     def login(username,db:Session):
#         user=db.query(User).filter(User.username==username).first()
#         return user

#     @staticmethod
#     def current_user_role(username,db:Session):
#         try:
#             user=db.query(User).filter(User.username==username).first()
#             if user:
#                 return user.role
#         except Exception as e:
#             logger.logging_error(f"Current Login User role not found {str(e)}")

#     @staticmethod
#     def update_user(id,schema_user,db:Session):
#         try:
#             user_query=db.query(User).filter(User.id==id)
#             user=user_query.first()
#             print(user)
#             if not user:
#                 print("user not found")
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
                
            
#             user_query.update(
#                 {
#                 "email":schema_user.email,
#                 "role":schema_user.role
#                 },synchronize_session=False )
#             db.commit()
#             db.refresh(user)
#             return {"message": "Employee updated successfully", "updated_employee": [f"email={user.email},role={user.role} on username={user.username}"]}
#         except IntegrityError as e:
#             db.rollback()
#             if "Duplicate entry" in str(e.orig):
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Email already exists. Please use a different one."
#                 )
#             raise HTTPException(status_code=400, detail="Database integrity error")
#         except Exception as e:
#             db.rollback()
#             logger.logging_error(f"Update User: {str(e)}")
#             raise HTTPException(status_code=500, detail=str(e))  

#     @staticmethod
#     def user_delete(id,db:Session):
#         user=db.query(User).filter(User.id==id).first()
#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {id} not found in the database")
#         db.query(User).filter(User.id==id).delete(synchronize_session=False)
#         db.commit()
#         return {"message": f"Employee with ID {id} has been successfully deleted"}
            



            
        
            
        