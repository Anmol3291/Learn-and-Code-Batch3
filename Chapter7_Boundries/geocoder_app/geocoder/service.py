import requests
from typing import Optional
from geocoder.config import Config
from geocoder.models import GeoLocation


class GeoCoderService:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def get_coordinates(self, place_name: str) -> Optional[GeoLocation]:
        try:
            params = {"q": place_name, "api_key": self.api_key}
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data:
                lat = data[0].get("lat")
                lon = data[0].get("lon")
                return GeoLocation(lat, lon)
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except (KeyError, IndexError, ValueError) as e:
            print(f"Data parsing error: {e}")
        return None
