# fastapi_crud_with_global_authentication
It's a crud operations fastapi project with global authentication with JWT token authentication 

1st need to activate virtual enviroment myenv/Scrips/activate
install reqirements it's in requirements.txt

** Project Structure

multi_tenant_fastapi/sec/

│── main.py  
│── database.py  
|-- dependencies.py
│── config/
│   │── config.py  
│── models/
│   │── base.py  
│   │── user.py  
│  
│── schemas/
│   │── user.py  
│   
│── services/
│   │── user_service.py  
│   
│── repository/
│   │── user_repository.py  
│     
│── controllers/
│   │── users.py  
│   
│── routes/
│   │── route.py  
│── utils/
│   │── security.py  
│   │── logger.py  
|   |-- token.py
│   
│── myenv  
│── requirements.txt  


To run the app => uvicorn src.main:app --reload
