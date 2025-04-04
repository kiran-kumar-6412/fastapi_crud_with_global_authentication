import logging


#stores the erros in errors.log file
logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s-%(levelname)s-%(message)s"
)

def logging_error(message:str):
    try:
        logging.error(message)
    except Exception as e:
        print(f"logging Errror {str(e)}")