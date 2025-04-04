from fastapi import APIRouter
from src.controller.user_routes import router as user_router
import src.utils.logger as logger

router = APIRouter()

try:
    router.include_router(user_router, tags=["users"], prefix="/users")
except Exception as e:
    error_msg = f"Error Including User Routes: {str(e)}"
    logger.logging_error(error_msg)
    raise RuntimeError(error_msg)  # 🚀 Raise the error so FastAPI fails early
