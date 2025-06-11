# # import overpy
# # import requests
# # import logging
# # from typing import List, Dict, Tuple
# # from concurrent.futures import ThreadPoolExecutor
# # import os
# # import googlemaps

# # logger = logging.getLogger(__name__)

# # # class DetectionService:
# # #     def __init__(self):
# # #         self.overpy_api = overpy.Overpass()
# # #         self.api_base_url = "https://reportallusa.com/api/parcels"
# # #         self.client_key =  os.getenv("REPORT_ALL_KEY", "sGeU2WMrgB")
# # #         self.api_version = "9"

# # #     def get_water_bodies(self, lat: float, lon: float, radius: int = 1000):
# # #         """
# # #         Fetch water bodies within a specified radius of given latitude and longitude.

# # #         Args:
# # #             lat (float): Latitude of the center point.
# # #             lon (float): Longitude of the center point.
# # #             radius (int): Radius in meters to search for water bodies.

# # #         Returns:
# # #             list: A list of tuples containing latitude and longitude of water bodies.
# # #         """
# # #         try:
# # #             query = f"""
# # #             (
# # #             node(around:{radius},{lat},{lon})["natural"="water"];
# # #             way(around:{radius},{lat},{lon})["natural"="water"];
# # #             relation(around:{radius},{lat},{lon})["natural"="water"];
# # #             way(around:{radius},{lat},{lon})["water"~".*"];
# # #             relation(around:{radius},{lat},{lon})["water"~".*"];
# # #             );
# # #             out center;
# # #             """
# # #             result = self.overpy_api.query(query)
# # #             water_bodies = []

# # #             # Collect coordinates from nodes
# # #             for node in result.nodes:
# # #                 water_bodies.append((node.lat, node.lon))

# # #             # Collect coordinates from ways and relations (center point)
# # #             for way in result.ways:
# # #                 if way.center_lat and way.center_lon:
# # #                     water_bodies.append((way.center_lat, way.center_lon))

# # #             for rel in result.relations:
# # #                 if rel.center_lat and rel.center_lon:
# # #                     water_bodies.append((rel.center_lat, rel.center_lon))

# # #             # Return the enriched data with parcel information
# # #             return self.get_parcels_for_water_bodies(water_bodies)

# # #         except Exception as e:
# # #             logger.error(f"Error fetching water bodies: {e}")
# # #             return []
    
    
# # class DetectionService:
# #     def __init__(self):
# #         # Initialize Google Maps client with your API key
# #         self.gmaps = googlemaps.Client(key=os.getenv('GOOGLE_PLACES_API_KEY'))
# #         self.api_base_url = "https://reportallusa.com/api/parcels"
# #         self.client_key = os.getenv("REPORT_ALL_KEY", "sGeU2WMrgB")
# #         self.api_version = "9"

# #     def get_water_bodies(self, lat: float, lon: float, radius: int = 1000):
# #         """
# #         Fetch water bodies within a specified radius of given latitude and longitude using Google Places API.

# #         Args:
# #             lat (float): Latitude of the center point.
# #             lon (float): Longitude of the center point.
# #             radius (int): Radius in meters to search for water bodies.

# #         Returns:
# #             list: A list of water bodies with their coordinates and parcel data.
# #         """
# #         try:
# #             # Search for water-related places
# #             places_result = self.gmaps.places_nearby(
# #                 location=(lat, lon),
# #                 radius=radius,
# #                 keyword='water',
# #                 type=['natural_feature']
# #             )

# #             water_bodies = []

# #             # Extract locations from results
# #             if places_result.get('results'):
# #                 for place in places_result['results']:
# #                     location = place['geometry']['location']
# #                     water_bodies.append((
# #                         location['lat'],
# #                         location['lng']
# #                     ))

# #                 # Handle pagination if there are more results
# #                 while 'next_page_token' in places_result:
# #                     # Wait briefly before requesting next page (API requirement)
# #                     time.sleep(2)
# #                     places_result = self.gmaps.places_nearby(
# #                         location=(lat, lon),
# #                         radius=radius,
# #                         keyword='water',
# #                         type=['natural_feature'],
# #                         page_token=places_result['next_page_token']
# #                     )
                    
# #                     for place in places_result.get('results', []):
# #                         location = place['geometry']['location']
# #                         water_bodies.append((
# #                             location['lat'],
# #                             location['lng']
# #                         ))

# #             # Return the enriched data with parcel information
# #             return self.get_parcels_for_water_bodies(water_bodies)

# #         except Exception as e:
# #             logger.error(f"Error fetching water bodies from Google Places API: {e}")
# #             return []
    
# #     def fetch_parcel_data(self, lat: float, lon: float) -> Dict:
# #         """Fetch parcel data for a single coordinate point"""
# #         try:
# #             params = {
# #                 "client": self.client_key,
# #                 "v": self.api_version,
# #                 "spatial_intersect": f"POINT({lon} {lat})",
# #                 "si_srid": "4326"
# #             }
# #             # response = requests.get(self.api_base_url+"?client=sGeU2WMrgB&v=9&spatial_intersect=POINT("+str(lon)+"%20"+str(lat)+")&si_srid=4326", timeout=10)
# #             response = requests.get(self.api_base_url, params=params, timeout=10)
# #             response.raise_for_status()
            
# #             data = response.json()
# #             return data['results']
            
# #         except Exception as e:
# #             logging.error(f"Error fetching parcel data for {lat},{lon}: {str(e)}")
# #             return {"error": str(e)}

# #     def get_parcels_for_water_bodies(
# #         self, 
# #         water_body_coords: List[Tuple[float, float]]
# #     ) -> List[Dict]:
# #         """
# #         Fetch parcel data for multiple water body coordinates
        
# #         Args:
# #             water_body_coords: List of (lat, lon) tuples from DetectionService
            
# #         Returns:
# #             List of dictionaries with water body coordinates and parcel data
# #         """
# #         results = []
        
# #         with ThreadPoolExecutor(max_workers=5) as executor:
# #             futures = []
# #             for lat, lon in water_body_coords:
# #                 futures.append(executor.submit(self.fetch_parcel_data, lat, lon))
            
# #             for i, future in enumerate(futures):
# #                 result = {
# #                     "water_body_coordinates": water_body_coords[i],
# #                     "parcel_data": future.result()
# #                 }
# #                 results.append(result)
        
# #         return results  
    
    
# import googlemaps
# import requests
# import logging
# import time
# from typing import List, Dict, Tuple
# from concurrent.futures import ThreadPoolExecutor
# import os

# logger = logging.getLogger(__name__)

# class DetectionService:
#     def __init__(self):
#         # Initialize Google Maps client with your API key
#         self.gmaps = googlemaps.Client(key=os.getenv('GOOGLE_PLACES_API_KEY'))
#         self.api_base_url = "https://reportallusa.com/api/parcels"
#         self.client_key = os.getenv("REPORT_ALL_KEY", "sGeU2WMrgB")
#         self.api_version = "9"

#     def get_water_bodies(self, lat: float, lon: float, radius: int = 1000):
#         """
#         Fetch water bodies within a specified radius of given latitude and longitude using Google Places API.

#         Args:
#             lat (float): Latitude of the center point.
#             lon (float): Longitude of the center point.
#             radius (int): Radius in meters to search for water bodies.

#         Returns:
#             list: A list of water bodies with their coordinates and parcel data.
#         """
#         try:
#             # Search for water-related places using multiple types to increase coverage
#             water_bodies = []
            
#             # Search for natural features (lakes, rivers)
#             places_result = self.gmaps.places_nearby(
#                 location=(lat, lon),
#                 radius=radius,
#                 keyword='lake pond water reservoir',
#                 type='establishment'
#             )
            
#             # Process results
#             self._extract_locations(places_result, water_bodies)
            
#             # Handle pagination
#             self._handle_pagination(places_result, water_bodies, lat, lon, radius)
            
#             # Also search for just "water" to get better coverage
#             places_result = self.gmaps.places_nearby(
#                 location=(lat, lon),
#                 radius=radius,
#                 keyword='lake OR pond OR river OR reservoir',
#             )
            
#             # Process results
#             self._extract_locations(places_result, water_bodies)
            
#             # Handle pagination
#             self._handle_pagination(places_result, water_bodies, lat, lon, radius)

#             # Return the enriched data with parcel information
#             return self.get_parcels_for_water_bodies(water_bodies)

#         except Exception as e:
#             logger.error(f"Error fetching water bodies from Google Places API: {e}")
#             return []
    
#     def _extract_locations(self, places_result, water_bodies):
#         """Helper method to extract locations from places API results"""
#         if places_result.get('results'):
#             for place in places_result['results']:
#                 location = place['geometry']['location']
#                 water_body = (
#                     location['lat'],
#                     location['lng']
#                 )
#                 # Avoid duplicates
#                 if water_body not in water_bodies:
#                     water_bodies.append(water_body)
    
#     def _handle_pagination(self, places_result, water_bodies, lat, lon, radius):
#         """Helper method to handle pagination in places API results"""
#         while 'next_page_token' in places_result:
#             # Wait briefly before requesting next page (API requirement)
#             time.sleep(2)
#             try:
#                 places_result = self.gmaps.places_nearby(
#                     page_token=places_result['next_page_token']
#                 )
#                 self._extract_locations(places_result, water_bodies)
#             except Exception as e:
#                 logger.error(f"Error handling pagination: {e}")
#                 break
    
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
        
#         return results


import googlemaps
import requests
import logging
import time
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class DetectionService:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Google Maps client with your API key
        api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        print(f"Initializing with API key: {api_key[:5]}...{api_key[-4:] if api_key else 'None'}")
        
        self.gmaps = googlemaps.Client(key=api_key)
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
        print(f"Searching for water bodies at: {lat}, {lon} with radius {radius}m")
        try:
            # Search for water-related places using multiple types to increase coverage
            water_bodies = []
            
            # Search for natural features (lakes, rivers)
            print("Searching with keyword='lake pond water reservoir', type='establishment'")
            places_result = self.gmaps.places_nearby(
                location=(lat, lon),
                radius=radius,
                keyword='lake pond water reservoir',
                type='establishment'
            )
            
            # Print API response status
            print(f"API response status: {places_result.get('status', 'unknown')}")
            print(f"Found {len(places_result.get('results', []))} results in first query")
            
            # Process results
            self._extract_locations(places_result, water_bodies)
            
            # Handle pagination
            self._handle_pagination(places_result, water_bodies, lat, lon, radius)
            
            # Also search for just "water" to get better coverage
            print("Searching with keyword='lake OR pond OR river OR reservoir'")
            places_result = self.gmaps.places_nearby(
                location=(lat, lon),
                radius=radius,
                keyword='lake OR pond OR river OR reservoir',
            )
            
            print(f"API response status: {places_result.get('status', 'unknown')}")
            print(f"Found {len(places_result.get('results', []))} results in second query")
            
            # Process results
            self._extract_locations(places_result, water_bodies)
            
            # Handle pagination
            self._handle_pagination(places_result, water_bodies, lat, lon, radius)
            
            # Also try text search which sometimes works better
            print("Trying text search for 'lake'")
            places_result = self.gmaps.places(
                query='lake',
                location=(lat, lon),
                radius=radius
            )
            
            print(f"Text search found {len(places_result.get('results', []))} results")
            self._extract_locations(places_result, water_bodies)

            print(f"Total unique water bodies found: {len(water_bodies)}")

            # Return the enriched data with parcel information
            return self.get_parcels_for_water_bodies(water_bodies)

        except Exception as e:
            logger.error(f"Error fetching water bodies from Google Places API: {e}")
            print(f"Error: {e}")
            return []
    
    def _extract_locations(self, places_result, water_bodies):
        """Helper method to extract locations from places API results"""
        if places_result.get('results'):
            for place in places_result['results']:
                location = place['geometry']['location']
                water_body = (
                    location['lat'],
                    location['lng']
                )
                # Avoid duplicates
                if water_body not in water_bodies:
                    water_bodies.append(water_body)
                    print(f"Found water body at: {water_body[0]}, {water_body[1]} - {place.get('name', 'Unknown')}")
    
    def _handle_pagination(self, places_result, water_bodies, lat, lon, radius):
        """Helper method to handle pagination in places API results"""
        while 'next_page_token' in places_result:
            # Wait briefly before requesting next page (API requirement)
            time.sleep(2)
            try:
                places_result = self.gmaps.places_nearby(
                    page_token=places_result['next_page_token']
                )
                print(f"Pagination returned {len(places_result.get('results', []))} additional results")
                self._extract_locations(places_result, water_bodies)
            except Exception as e:
                logger.error(f"Error handling pagination: {e}")
                print(f"Pagination error: {e}")
                break
    
    def fetch_parcel_data(self, lat: float, lon: float) -> Dict:
        """Fetch parcel data for a single coordinate point"""
        try:
            params = {
                "client": self.client_key,
                "v": self.api_version,
                "spatial_intersect": f"POINT({lon} {lat})",
                "si_srid": "4326"
            }
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
        
    def find_water_bodies(self, locations=None):
        """
        Standalone method to search for water bodies in specified locations
        and print their coordinates
        
        Args:
            locations: Optional list of dictionaries with name, lat, lon keys.
                      If None, uses default test locations.
        """
        # Default test locations if none provided
        if locations is None:
            locations = [
                {"name": "Lake Michigan area", "lat": 41.8781, "lon": -87.6298},  # Chicago
                {"name": "Florida Everglades", "lat": 25.2866, "lon": -80.8987},
                {"name": "Central Park NYC", "lat": 40.7812, "lon": -73.9665}
            ]
        
        # Search radius in meters
        radius = 1000  # 5km radius
        
        print("==== Water Bodies Finder ====")
        
        for location in locations:
            print(f"\nSearching for water bodies near {location['name']}...")
            print(f"Coordinates: {location['lat']}, {location['lon']}")
            print(f"Search radius: {radius} meters")
            
            # Get water bodies
            start_time = time.time()
            water_bodies = self.get_water_bodies(
                lat=location['lat'], 
                lon=location['lon'], 
                radius=radius
            )
            elapsed_time = time.time() - start_time
            
            # Print results
            print(f"Found {len(water_bodies)} water bodies in {elapsed_time:.2f} seconds:")
            
            if water_bodies:
                for i, water_body in enumerate(water_bodies, 1):
                    coords = water_body.get('water_body_coordinates', ('N/A', 'N/A'))
                    print(f"  {i}. Water body at: {coords[0]}, {coords[1]}")
                    
                    # Print first parcel info if available
                    parcel_data = water_body.get('parcel_data', [])
                    if parcel_data and isinstance(parcel_data, list) and len(parcel_data) > 0:
                        parcel = parcel_data[0]
                        print(f"     Parcel info: {parcel.get('address', 'No address')} - {parcel.get('owner_name', 'Unknown owner')}")
            else:
                print("  No water bodies found in this area.")
            
            print("-" * 50)
            
        return "Water body search complete"


# Simple test function to run when file is executed directly
if __name__ == "__main__":
    service = DetectionService()
    
    # Test with custom location - adjust these coordinates as needed
    custom_location = [
        {"name": "Your Location", "lat": 34.0522, "lon": -118.2437}  # Los Angeles - change to your coordinates
    ]
    
    service.find_water_bodies(custom_location)