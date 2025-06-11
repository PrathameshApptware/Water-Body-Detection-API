import overpy
import requests
import logging
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
import os

logger = logging.getLogger(__name__)

# class DetectionService:
#     def __init__(self):
#         self.overpy_api = overpy.Overpass()
#         self.api_base_url = "https://reportallusa.com/api/parcels"
#         self.client_key =  os.getenv("REPORT_ALL_KEY", "sGeU2WMrgB")
#         self.api_version = "9"

#     def get_water_bodies(self, lat: float, lon: float, radius: int = 1000):
#         """
#         Fetch water bodies within a specified radius of given latitude and longitude.

#         Args:
#             lat (float): Latitude of the center point.
#             lon (float): Longitude of the center point.
#             radius (int): Radius in meters to search for water bodies.

#         Returns:
#             list: A list of tuples containing latitude and longitude of water bodies.
#         """
#         try:
#             query = f"""
#             (
#             node(around:{radius},{lat},{lon})["natural"="water"];
#             way(around:{radius},{lat},{lon})["natural"="water"];
#             relation(around:{radius},{lat},{lon})["natural"="water"];
#             way(around:{radius},{lat},{lon})["water"~".*"];
#             relation(around:{radius},{lat},{lon})["water"~".*"];
#             );
#             out center;
#             """
#             result = self.overpy_api.query(query)
#             water_bodies = []

#             # Collect coordinates from nodes
#             for node in result.nodes:
#                 water_bodies.append((node.lat, node.lon))

#             # Collect coordinates from ways and relations (center point)
#             for way in result.ways:
#                 if way.center_lat and way.center_lon:
#                     water_bodies.append((way.center_lat, way.center_lon))

#             for rel in result.relations:
#                 if rel.center_lat and rel.center_lon:
#                     water_bodies.append((rel.center_lat, rel.center_lon))

#             # Return the enriched data with parcel information
#             return self.get_parcels_for_water_bodies(water_bodies)

#         except Exception as e:
#             logger.error(f"Error fetching water bodies: {e}")
#             return []
    
    
class DetectionService:
    def __init__(self):
        # Initialize Google Maps client with your API key
        self.gmaps = googlemaps.Client(key=os.getenv('GOOGLE_PLACES_API_KEY'))
        self.api_base_url = "https://reportallusa.com/api/parcels"
        self.client_key = os.getenv("REPORT_ALL_KEY", "sGeU2WMrgB")
        self.api_version = "9"

    def get_water_bodies(self, lat: float, lon: float, radius: int = 1000):
        """
        Fetch water bodies within a specified radius of given latitude and longitude using Google Places API.

        Args:
            lat (float): Latitude of the center point.
            lon (float): Longitude of the center point.
            radius (int): Radius in meters to search for water bodies.

        Returns:
            list: A list of water bodies with their coordinates and parcel data.
        """
        try:
            # Search for water-related places
            places_result = self.gmaps.places_nearby(
                location=(lat, lon),
                radius=radius,
                keyword='water',
                type=['natural_feature']
            )

            water_bodies = []

            # Extract locations from results
            if places_result.get('results'):
                for place in places_result['results']:
                    location = place['geometry']['location']
                    water_bodies.append((
                        location['lat'],
                        location['lng']
                    ))

                # Handle pagination if there are more results
                while 'next_page_token' in places_result:
                    # Wait briefly before requesting next page (API requirement)
                    time.sleep(2)
                    places_result = self.gmaps.places_nearby(
                        location=(lat, lon),
                        radius=radius,
                        keyword='water',
                        type=['natural_feature'],
                        page_token=places_result['next_page_token']
                    )
                    
                    for place in places_result.get('results', []):
                        location = place['geometry']['location']
                        water_bodies.append((
                            location['lat'],
                            location['lng']
                        ))

            # Return the enriched data with parcel information
            return self.get_parcels_for_water_bodies(water_bodies)

        except Exception as e:
            logger.error(f"Error fetching water bodies from Google Places API: {e}")
            return []
    
    def fetch_parcel_data(self, lat: float, lon: float) -> Dict:
        """Fetch parcel data for a single coordinate point"""
        try:
            params = {
                "client": self.client_key,
                "v": self.api_version,
                "spatial_intersect": f"POINT({lon} {lat})",
                "si_srid": "4326"
            }
            # response = requests.get(self.api_base_url+"?client=sGeU2WMrgB&v=9&spatial_intersect=POINT("+str(lon)+"%20"+str(lat)+")&si_srid=4326", timeout=10)
            response = requests.get(self.api_base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data['results']
            
        except Exception as e:
            logging.error(f"Error fetching parcel data for {lat},{lon}: {str(e)}")
            return {"error": str(e)}

    def get_parcels_for_water_bodies(
        self, 
        water_body_coords: List[Tuple[float, float]]
    ) -> List[Dict]:
        """
        Fetch parcel data for multiple water body coordinates
        
        Args:
            water_body_coords: List of (lat, lon) tuples from DetectionService
            
        Returns:
            List of dictionaries with water body coordinates and parcel data
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for lat, lon in water_body_coords:
                futures.append(executor.submit(self.fetch_parcel_data, lat, lon))
            
            for i, future in enumerate(futures):
                result = {
                    "water_body_coordinates": water_body_coords[i],
                    "parcel_data": future.result()
                }
                results.append(result)
        
        return results  
    