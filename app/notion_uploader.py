"""
This module provides a service class to upload house information to a Notion database.

The NotionUploaderService class uses the Notion API to add house listings found on Funda to a 
specified Notion database.

Dependencies:
    requests
    house (for the House class)

Environment Variables:
    NOTION_SECRET: The secret key for Notion API access.
    NOTION_DATABASE_ID: The ID of the Notion database where house data will be uploaded.

Classes:
    NotionUploaderService: A service class to handle uploading house data to Notion.

Methods in NotionUploaderService:
    add_houses(found_houses: list) -> None: Adds a list of found houses to the Notion 
      database.
"""

import requests
from house import House

class NotionUploaderService:
    """
    A service class to upload house information to a Notion database.

    This class uses the Notion API to add house listings found on Funda to a specified Notion
    database.

    Attributes:
        headers (dict): Headers required for the Notion API requests.

    Methods:
        check_house(house: House) -> bool:
            Checks if a house is already present in the Notion database.
        add_houses(found_houses: list) -> None:
            Adds a list of found houses to the Notion database.
    """

    def __init__(self, notion_secret, notion_database_id) -> None:
        """
        Initializes the NotionUploaderService with the necessary headers for API requests.
        """
        self.database_id = notion_database_id
        self.headers = {
            "Authorization": f"Bearer {notion_secret}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def check_house(self, house: House) -> bool:
        """
        Checks if a house is already present in the Notion database.

        Args:
            house (House): The house object to check in the Notion database.

        Returns:
            bool: True if the house is found in the Notion database, False otherwise.
        """
        query_url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        query_payload = {
            "filter": {"property": "House ID", "title": {"equals": house.id}}
        }

        response = requests.post(
            query_url, headers=self.headers, json=query_payload, timeout=60
        )

        response.raise_for_status()
        return bool(response.json()["results"])

    def add_houses(self, found_houses: list) -> None:
        """
        Adds a list of found houses from Funda to the Notion database.

        Args:
            found_houses (list): List of found houses from Funda.
        """
        for house in found_houses:
            if self.check_house(house):
                print(f"House ID {house.id} already exists in the database.")
                continue

            create_url = "https://api.notion.com/v1/pages"

            create_payload = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "House ID": {"title": [{"text": {"content": str(house.id)}}]},
                    "URL": {"url": house.url},
                    "Post Address": {
                        "rich_text": [{"text": {"content": house.address.full}}]
                    },
                    "City": {"rich_text": [{"text": {"content": house.address.city}}]},
                    "Price": {"number": house.price},
                    "ZIP Code": {
                        "rich_text": [{"text": {"content": house.address.zip_code}}]
                    },
                    "Time to office S.": {
                        "rich_text": [{"text": {"content": house.s_office_travel_time}}]
                    },
                    "Time to office V.": {
                        "rich_text": [{"text": {"content": house.v_office_travel_time}}]
                    },
                    "Life Level Score": {"number": house.life_level_score},
                },
            }

            response = requests.post(
                create_url, headers=self.headers, json=create_payload, timeout=60
            )

            try:
                response.raise_for_status()
                print(f"New house with ID {house.id} added to the database.")
            except requests.exceptions.HTTPError as e:
                print(
                    f"Error creating entry for House ID {house.id}: {e.response.text}"
                )
