from vehicle_service_center.interfaces.vehicle_service import VehicleService


class BikeService(VehicleService):
    """Implementation of vehicle service operations for bikes."""

    def services(self):
        """Perform chain lubrication and brake tightening service for bike."""
        print("Bike Service: Chain lubrication, Brake tightening.")
