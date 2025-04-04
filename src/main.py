from fastapi import FastAPI
from src.routes.route import router  # ✅ Absolute Import
from src.models.base import Base
from src.database import engine
import src.utils.logger as logger

app = FastAPI()

try:
    Base.metadata.create_all(bind=engine)  # ✅ Creates tables if not exist
    app.include_router(router)  # ✅ Include API routes
except Exception as e:
    logger.logging_error(f"Error Initializing App: {str(e)}")  # ✅ Logging
