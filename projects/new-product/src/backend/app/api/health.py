"""Health check endpoint."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    
    Returns:
        dict: Health status of the application and its dependencies
    """
    health_status = {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat(),
        "dependencies": {}
    }
    
    # Check database connectivity
    try:
        db.execute(text("SELECT 1"))
        health_status["dependencies"]["database"] = "healthy"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["dependencies"]["database"] = f"unhealthy: {str(e)}"
    
    return health_status
