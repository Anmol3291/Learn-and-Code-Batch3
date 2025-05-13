class GeoLocation:
    def __init__(self, latitude: str, longitude: str):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"Latitude: {self.latitude}\nLongitude: {self.longitude}"
