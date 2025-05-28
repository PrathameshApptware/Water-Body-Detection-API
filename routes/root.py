from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def root():
    """
    Check if the API is running.
    
    Returns:
    
        dict: A status message indicating the API is online
    """
    return {"status": "online", "message": "Resume Screening API is running"}