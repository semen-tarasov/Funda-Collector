"""
Collector module for gathering and managing house data from various sources.

This module defines classes and methods to collect house data, including:
- Initialization of services
- Data collection from Funda
- Uploading data to Notion

Dependencies:
    os
    dotenv
    funda.FundaService
    location.LocationService
    life_level.LifeLevelScoreService
    notion_uploader.NotionUploaderService
    house.Address
    house.House

Classes:
    App: Main application class for collecting and managing house data.

Methods in App:
    __init__(notion_uploader_service: NotionUploaderService, life_level_service: 
    LifeLevelScoreService, location_service: LocationService, 
    funda_service: FundaService) -> None: Initializes the App class with the given services.
    create_house(house_id: int, house_dict: dict) -> House: Creates a House object from provided 
    house details.
    run_search_and_upload() -> None: Runs the search for houses and uploads them to Notion.
"""

from funda import FundaService
from location import LocationService
from life_level import LifeLevelScoreService
from notion_uploader import NotionUploaderService

from house import Address, House

class App:
    """
    A class to hold the different services used in the application.

    Attributes:
        notion_uploader (NotionUploaderService): Service to upload houses to Notion.
        life_level (LifeLevelScoreService): Service to retrieve life level scores.
        location (LocationService): Service to interact with Google Maps API.
        funda (FundaService): Service to search for houses on Funda.
    """

    def __init__(
        self,
        notion_uploader_service: NotionUploaderService,
        life_level_service: LifeLevelScoreService,
        location_service: LocationService,
        funda_service: FundaService,
        office_s: str,
        office_v: str,
    ) -> None:
        """
        Initializes the App class with the given services.

        Args:
            notion_uploader_service (NotionUploaderService): Service to upload houses to Notion.
            life_level_service (LifeLevelScoreService): Service to retrieve life level scores.
            location_service (LocationService): Service to interact with Google Maps API.
            funda_service (FundaService): Service to search for houses on Funda.
        """
        self.notion_uploader = notion_uploader_service
        self.life_level = life_level_service
        self.location = location_service
        self.funda = funda_service
        self.office_s = office_s
        self.office_v = office_v

    def create_house(
        self,
        house_id: int,
        house_dict: dict,
    ) -> House:
        """
        Creates a House object from provided house details.

        Args:
            house_id (int): The unique identifier for the house.
            house_dict (dict): A dictionary containing details about the house, including:
                - url (str): The URL of the house listing.
                - price (int): The price of the house.
                - address (Address): The short form of the house address.
                - city (str): The city where the house is located.

        Returns:
            House: A House object with the provided details and additional calculated attributes.
        """
        address_full = f"{house_dict['address']}, {house_dict['city']}, Netherlands"

        zip_code = self.location.get_zip_code(address_full)
        life_level_score = self.life_level.get_score(zip_code)

        s_office_travel_time = self.location.get_travel_time(address_full, self.office_s)
        v_office_travel_time = self.location.get_travel_time(address_full, self.office_v)

        house = House(
            id=house_id,
            url=house_dict["url"],
            price=house_dict["price"],
            address=Address(
                short=house_dict["address"],
                full=address_full,
                city=house_dict["city"],
                zip_code=zip_code,
            ),
            s_office_travel_time=s_office_travel_time,
            v_office_travel_time=v_office_travel_time,
            life_level_score=life_level_score,
        )

        return house

    def run_search_and_upload(self) -> None:
        """
        Runs the search for houses and uploads them to Notion.
        """
        funda_houses = []

        for city in self.funda.cities.split(","):
            funda_listings = self.funda.search(city)

            if funda_listings:
                for listing_id, listing_dict in funda_listings.items():
                    funda_houses.append(self.create_house(listing_id, listing_dict))

        print(f"\nFound {len(funda_houses)} houses.\n")
        self.notion_uploader.add_houses(funda_houses)

        return funda_houses


if __name__ == "__main__":
    app = App(
        notion_uploader_service=NotionUploaderService(),
        life_level_service=LifeLevelScoreService(),
        location_service=LocationService(),
        funda_service=FundaService(),
    )

    app.run_search_and_upload()
