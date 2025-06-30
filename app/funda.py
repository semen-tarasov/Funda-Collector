"""
This module provides a service to search for houses on Funda.

It includes a service class to search for houses in a 
specified city on Funda, retrieving the search results as a dictionary.

Dependencies:
    re
    funda_scraper (for the FundaScraper class)

Classes:
    FundaService: A service class to search for houses on Funda.

Methods in FundaService:
    search(city: str, type: str, min_price: int, max_price: int, days_since: int, property_type: str) -> dict: 
      Searches for houses on Funda in the specified city and returns the results as a dictionary.
"""

import re
from dataclasses import dataclass
from funda_scraper import FundaScraper

@dataclass
class FundaService:
    """
    A service class to search for houses on Funda.

    This class provides functionality to search for houses in a specified city on Funda
    and retrieve the search results as a dictionary.

    Methods:
        search(city: str, type: str, min_price: int, max_price: int, days_since: int, property_type: str) -> dict:
            Searches for houses on Funda in the specified city and returns the results as a
            dictionary.
    """
    def __init__ (self, cities: str, type: str, min_price: int, max_price: int, days_since: int, property_type: str) -> None:
        """
        Initializes the FundaService with the specified search parameters.
        """
        self.cities = cities
        self.type = type.lower()
        self.min_price = min_price
        self.max_price = max_price
        self.days_since = days_since
        self.property_type = property_type.lower()

    def search(self, city: str) -> dict:
        """
        Searches for houses on Funda in the specified city.

        Args:
            city (str): The city to search for houses.
            type (str): The type of search (e.g., "buy" or "rent").
            min_price (int): The minimum price for the search.
            max_price (int): The maximum price for the search.
            days_since (int): The number of days since the houses were listed.
            property_type (str): The type of property to search for (e.g., "house", "apartment").

        Returns:
            dict: A dictionary with house information from Funda in the specified city.

        Raises:
            ValueError: If house ID, address, or price cannot be extracted from the search results.
        """
        scraper = FundaScraper(
            area=city,
            want_to=str(self.type),
            page_start=1,
            n_pages=100,
            min_price=int(self.min_price),
            max_price=int(self.max_price),
            days_since=int(self.days_since),
            find_past=False,
            property_type=str(self.property_type),
        )

        search_results_dict = {}
        search_results = scraper.run(raw_data=True)
        search_results_raw_data = search_results.to_dict()

        i = 0
        if not search_results.empty:
            while True:
                url = search_results_raw_data["url"][i]
                price_str = search_results_raw_data["date_list"][i]

                patterns = {
                    "id": r"huis-(\d+)-",
                    "city": r"koop/([^/]+)/",
                    "price": r"€\s*([\d.]+)",
                    "address": r"huis-\d+-(.+?)/",
                }

                matches = {
                    "id": re.search(patterns["id"], url),
                    "city": re.search(patterns["city"], url),
                    "address": re.search(patterns["address"], url),
                    "price": re.search(patterns["price"], price_str),
                }

                if matches["id"] and matches["price"] and matches["address"]:
                    house_id = matches["id"].group(1)
                    house_dict = {
                        "url": url,
                        "city": " ".join(
                            word.capitalize()
                            for word in matches["city"].group(1).split("-")
                        ),
                        "address": " ".join(
                            word.capitalize()
                            for word in matches["address"].group(1).split("-")
                        ),
                        "price": int(matches["price"].group(1).replace(".", "")),
                    }

                    search_results_dict.setdefault(house_id, house_dict)

                else:
                    raise ValueError(
                        f"Can't get house ID, address, or price from link {url}."
                    )

                i += 1
                if i == len(search_results_raw_data["url"]):
                    return search_results_dict

        return None
