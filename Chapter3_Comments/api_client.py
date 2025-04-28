import requests
import json


class APIClient:
    """Handles API requests."""

    def fetch_data(self, url):
        try:
            response = requests.get(url)
            json_response = (
                response.text.replace("var tumblr_api_read = ", "")
                .strip()
                .replace(";", "")
            )
            return json.loads(json_response)
        except Exception as error:
            print(f"Error occurred while fetching data: {error}")
            return None
