from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import root, waterbody_detector
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Waterbodies Detection API",
    description="""
    This API allows you to get the co-ordinates of waterbodies within a 1km radius of given lat and lan.
    It also return their respective parcel data.
    
    ## Features
    
    * Detects waterbodies within a 1km radius of given lat and lan.
    * Returns the co-ordinates of the waterbodies.
    * Returns the respective parcel data.
    """,
    version="1.0.0",
    license_info={
        "name": "Private",
    },
    openapi_tags=[
        {
            "name": "Health",
            "description": "API health checking operations",
        },
        {
            "name": "Waterbodies Detection",
            "description": "Detects waterbodies within a 1km radius of given latitude and longitude and return their parcel data.",
        },
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(root.router, tags=["Health"])
app.include_router(waterbody_detector.router, tags=["Waterbodies Detection"])

if __name__ == "__main__":
    import uvicorn
    logging.info("Waterbodies Detection API")
    uvicorn.run(app, host="0.0.0.0", port=8000)