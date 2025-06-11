import overpy
import requests
import logging
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
import os
import googlemaps

logger = logging.getLogger(__name__)

class DetectionService:
    def __init__(self):
        self.overpy_api = overpy.Overpass()
        self.api_base_url = "https://reportallusa.com/api/parcels"
        self.client_key =  os.getenv("REPORT_ALL_KEY", "sGeU2WMrgB")
        self.api_version = "9"

    def get_water_bodies(self, lat: float, lon: float, radius: int = 1000):
        """
        Fetch water bodies within a specified radius of given latitude and longitude.

        Args:
            lat (float): Latitude of the center point.
            lon (float): Longitude of the center point.
            radius (int): Radius in meters to search for water bodies.

        Returns:
            list: A list of tuples containing latitude and longitude of water bodies.
        """
        try:
            query = f"""
            (
            node(around:{radius},{lat},{lon})["natural"="water"];
            way(around:{radius},{lat},{lon})["natural"="water"];
            relation(around:{radius},{lat},{lon})["natural"="water"];
            way(around:{radius},{lat},{lon})["water"~".*"];
            relation(around:{radius},{lat},{lon})["water"~".*"];
            );
            out center;
            """
            result = self.overpy_api.query(query)
            water_bodies = []

            # Collect coordinates from nodes
            for node in result.nodes:
                water_bodies.append((node.lat, node.lon))

            # Collect coordinates from ways and relations (center point)
            for way in result.ways:
                if way.center_lat and way.center_lon:
                    water_bodies.append((way.center_lat, way.center_lon))

            for rel in result.relations:
                if rel.center_lat and rel.center_lon:
                    water_bodies.append((rel.center_lat, rel.center_lon))

            # Return the enriched data with parcel information
            return self.get_parcels_for_water_bodies(water_bodies)

        except Exception as e:
            logger.error(f"Error fetching water bodies: {e}")
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
    


# import googlemaps
# import requests
# import logging
# import time
# from typing import List, Dict, Tuple
# from concurrent.futures import ThreadPoolExecutor
# import os
# from dotenv import load_dotenv

# logger = logging.getLogger(__name__)

# class DetectionService:
#     def __init__(self):
#         # Load environment variables
#         load_dotenv()
        
#         # Initialize Google Maps client with your API key
#         api_key = os.getenv('GOOGLE_PLACES_API_KEY')
#         print(f"Initializing with API key: {api_key[:5]}...{api_key[-4:] if api_key else 'None'}")
        
#         self.gmaps = googlemaps.Client(key=api_key)
#         self.api_base_url = "https://reportallusa.com/api/parcels"
#         self.client_key = os.getenv("REPORT_ALL_KEY", "sGeU2WMrgB")
#         self.api_version = "9"

#     def get_water_bodies(self, lat: float, lon: float, radius: int = 1000):
#         """
#         Fetch water bodies within a specified radius of given latitude and longitude.
#         This function is a drop-in replacement for the overpy-based water body detection.

#         Args:
#             lat (float): Latitude of the center point.
#             lon (float): Longitude of the center point.
#             radius (int): Radius in meters to search for water bodies.

#         Returns:
#             list: A list of tuples containing latitude and longitude of water bodies.
#         """
#         try:
#             water_bodies = []
            
#             # Strategy 1: Use places_nearby API with water-related keywords
#             print(f"Searching for water bodies at {lat}, {lon} within {radius}m radius")
            
#             # Search for natural features - lakes, ponds, rivers
#             keywords = ['lake', 'pond', 'reservoir', 'river', 'creek', 'water']
            
#             for keyword in keywords:
#                 try:
#                     places_result = self.gmaps.places_nearby(
#                         location=(lat, lon),
#                         radius=radius,
#                         keyword=keyword,
#                         type='natural_feature'  # Focus on natural features
#                     )
                    
#                     if places_result.get('status') == 'OK':
#                         # Extract coordinates from results
#                         for place in places_result.get('results', []):
#                             if 'geometry' in place and 'location' in place['geometry']:
#                                 location = place['geometry']['location']
#                                 water_body = (float(location['lat']), float(location['lng']))
                                
#                                 # Avoid duplicates
#                                 if water_body not in water_bodies:
#                                     water_bodies.append(water_body)
#                                     print(f"Found water body '{place.get('name')}' at {water_body}")
                        
#                         # Handle pagination similar to how Overpy handles multiple results
#                         if 'next_page_token' in places_result:
#                             time.sleep(2)  # Required delay before requesting next page
#                             next_page = self.gmaps.places_nearby(
#                                 page_token=places_result['next_page_token']
#                             )
                            
#                             for place in next_page.get('results', []):
#                                 if 'geometry' in place and 'location' in place['geometry']:
#                                     location = place['geometry']['location']
#                                     water_body = (float(location['lat']), float(location['lng']))
#                                     if water_body not in water_bodies:
#                                         water_bodies.append(water_body)
#                                         print(f"Found water body '{place.get('name')}' at {water_body}")
                
#                 except Exception as keyword_error:
#                     print(f"Error searching for keyword '{keyword}': {keyword_error}")
            
#             # Strategy 2: Use text search as a backup method
#             try:
#                 for keyword in ['lake', 'pond']:
#                     places_result = self.gmaps.places(
#                         query=keyword,
#                         location=(lat, lon),
#                         radius=radius
#                     )
                    
#                     for place in places_result.get('results', []):
#                         if 'geometry' in place and 'location' in place['geometry']:
#                             location = place['geometry']['location']
#                             water_body = (float(location['lat']), float(location['lng']))
#                             if water_body not in water_bodies:
#                                 water_bodies.append(water_body)
#                                 print(f"Found water body '{place.get('name')}' from text search at {water_body}")
            
#             except Exception as text_search_error:
#                 print(f"Error in text search: {text_search_error}")
            
#             print(f"Total water bodies found: {len(water_bodies)}")
            
#             # Return the enriched data with parcel information, same as the original function
#             return self.get_parcels_for_water_bodies(water_bodies)

#         except Exception as e:
#             logger.error(f"Error fetching water bodies: {e}")
#             return []

#     def fetch_parcel_data(self, lat: float, lon: float) -> Dict:
#         """Fetch parcel data for a single coordinate point"""
#         try:
#             params = {
#                 "client": self.client_key,
#                 "v": self.api_version,
#                 "spatial_intersect": f"POINT({lon} {lat})",
#                 "si_srid": "4326"
#             }
#             response = requests.get(self.api_base_url, params=params, timeout=10)
#             response.raise_for_status()
            
#             data = response.json()
#             return data['results']
            
#         except Exception as e:
#             logging.error(f"Error fetching parcel data for {lat},{lon}: {str(e)}")
#             return {"error": str(e)}

#     def get_parcels_for_water_bodies(
#         self, 
#         water_body_coords: List[Tuple[float, float]]
#     ) -> List[Dict]:
#         """
#         Fetch parcel data for multiple water body coordinates
        
#         Args:
#             water_body_coords: List of (lat, lon) tuples from DetectionService
            
#         Returns:
#             List of dictionaries with water body coordinates and parcel data
#         """
#         results = []
        
#         if not water_body_coords:
#             print("No water body coordinates to fetch parcels for")
#             return results
            
#         print(f"Fetching parcel data for {len(water_body_coords)} water bodies")
        
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             futures = []
#             for lat, lon in water_body_coords:
#                 futures.append(executor.submit(self.fetch_parcel_data, lat, lon))
            
#             for i, future in enumerate(futures):
#                 result = {
#                     "water_body_coordinates": water_body_coords[i],
#                     "parcel_data": future.result()
#                 }
#                 results.append(result)
                
#                 # Print summary of parcel data for debugging
#                 parcel_data = result.get("parcel_data", [])
#                 if isinstance(parcel_data, list) and parcel_data:
#                     parcel = parcel_data[0]
#                     address = parcel.get('address', 'No address')
#                     print(f"Found parcel at {address} for water body at {water_body_coords[i]}")
        
#         return results

