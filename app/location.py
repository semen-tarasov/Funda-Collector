"""
This module provides a service class to interact with the Google Maps API for various geographical
and travel-related functionalities. It includes methods to get travel times between locations and 
to retrieve ZIP codes from addresses.

Dependencies:
    datetime
    googlemaps

Environment Variables:
    GOOGLE_API_KEY: Your Google Maps API key.

Classes:
    LocationService: A service class to handle interactions with the Google Maps API.

Methods in LocationService:
    get_departure_time() -> datetime: Creates a datetime object for departure at 8 AM the next 
      day.
    get_travel_time(origin: str, destination: str, mode="transit") -> str: Calculates travel time
      from origin to destination.
    get_zip_code(address: str) -> str: Gets the ZIP code for a given address.
"""

from datetime import datetime, timedelta
import googlemaps

class LocationService:
    """
    A class to interact with the Google Maps API for various geographical and travel-related
    functionalities.

    Methods:
        get_departure_time() -> datetime:
            Creates a datetime object for departure at 8 AM the next day.

        get_travel_time(origin: str, destination: str, mode="transit") -> str:
            Calculates travel time from origin to destination using the Google Maps API.

        get_zip_code(address: str) -> str:
            Gets the ZIP code for a given address using the Google Maps API.
    """

    def __init__(self, google_api_key) -> None:
        """
        Initializes the LocationService with a Google Maps API key.
        """
        self.gmaps = googlemaps.Client(key=google_api_key)
        self.departure_time = self.get_departure_time()

    @staticmethod
    def get_departure_time() -> datetime:
        """
        Creates a datetime object for departure at 8 AM the next day.

        Returns:
            datetime: Tomorrow at 8 AM as a datetime object.
        """
        today = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        return today + timedelta(days=1)

    def get_travel_time(self, origin: str, destination: str, mode="transit") -> str:
        """
        Calculates travel time from origin to destination using the Google Maps API.

        Args:
            origin (str): The starting point for travel.
            destination (str): The endpoint for travel.
            mode (str, optional): The mode of travel. Defaults to "transit".

        Returns:
            str: Duration of travel time if found, otherwise "TRAVEL TIME NOT FOUND".
        """
        distance_matrix = self.gmaps.distance_matrix(
            origin, destination, mode=mode, departure_time=self.departure_time
        )

        if distance_matrix["status"] == "OK":
            if "duration" in distance_matrix["rows"][0]["elements"][0]:
                return distance_matrix["rows"][0]["elements"][0]["duration"]["text"]
        return "TRAVEL TIME NOT FOUND"

    def get_zip_code(self, address: str) -> str:
        """
        Gets the ZIP code for a given address using the Google Maps API.

        Args:
            address (str): The full address to geocode.

        Returns:
            str: The ZIP code as a string if found, otherwise "ZIP CODE NOT FOUND".
        """
        geocode_result = self.gmaps.geocode(address)
        if geocode_result:
            for component in geocode_result[0]["address_components"]:
                if "postal_code" in component["types"]:
                    return component["long_name"]
        return "ZIP CODE NOT FOUND"
