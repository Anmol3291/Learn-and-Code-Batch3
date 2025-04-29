from geocoder.service import GeoCoderService
from geocoder.config import Config


def run_console():
    try:
        place = input("Enter place name: ").strip()
        if not place:
            print("Place name cannot be empty.")
            return

        service = GeoCoderService(Config.BASE_URL, Config.API_KEY)
        location = service.get_coordinates(place)

        if location:
            print("\nResult:\n" + str(location))
        else:
            print("Location not found. Please try a different place.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
