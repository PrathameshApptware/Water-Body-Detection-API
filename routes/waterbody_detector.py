from fastapi import APIRouter, Depends
from models.models import WaterBodyCoordinates
from services.detection_service import DetectionService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/detect_waterbodies")
async def detect_waterbodies(
    waterbody_coordinates: WaterBodyCoordinates,
    detection_service: DetectionService = Depends()
):
    """
    Detect water bodies within a 1km radius of given latitude and longitude.
        
    Args:
    
        lat (float): Latitude of the center point.
        lon (float): Longitude of the center point.
        radius (int, optional): Radius in meters to search for water bodies. Defaults to 1000.
        
    Returns:
    
        list: A list of tuples containing latitude and longitude of detected water bodies and their parcel data.
        
    Raises:
    
        HTTPException: If an error occurs while fetching water bodies.
    """
    return detection_service.get_water_bodies(
        lat=waterbody_coordinates.lat,
        lon=waterbody_coordinates.lon
    )
