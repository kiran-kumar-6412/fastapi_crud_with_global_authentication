import logging
from src.models.log import Log
from datetime import datetime

# #stores the erros in errors.log file if database faild
# logging.basicConfig(
#     filename="errors.log",
#     level=logging.ERROR,
#     format="%(asctime)s-%(levelname)s-%(message)s"
# )

# def logging_error(message:str):
#     try:
#         logging.error(message)
#     except Exception as e:
#         print(f"logging Errror {str(e)}")




#database 

def logging_error(message: str,level: str="ERROR"):
    try:
        #from src.models.log import Log
        from src.database import local_session
        db = local_session()
        log_entry = Log(
            level=level,
            message=message,
            created_at=datetime.utcnow()
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        print(f"⚠️ Failed to log to database: {str(e)}\nOriginal error: {message}")
    finally:
        db.close()
