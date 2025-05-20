from vehicle_service_center.services.car_service import CarService
from vehicle_service_center.services.bike_service import BikeService
from vehicle_service_center.services.truck_service import TruckService


class VehicleServiceFactory:

    @staticmethod
    def create_service(vehicle_type):
        vehicle_type = vehicle_type.lower()

        if vehicle_type == "car":
            return CarService()
        elif vehicle_type == "bike":
            return BikeService()
        elif vehicle_type == "truck":
            return TruckService()
        else:
            raise ValueError(f"Unsupported vehicle type: {vehicle_type}")
