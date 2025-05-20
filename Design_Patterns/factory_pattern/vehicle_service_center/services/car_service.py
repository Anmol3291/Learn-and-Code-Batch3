from vehicle_service_center.interfaces.vehicle_service import VehicleService


class CarService(VehicleService):
    """Implementation of vehicle service operations for cars."""

    def services(self):
        """Perform oil change, Brake inspection and Tire rotation service for car."""
        return print("Car Service: Oil change, Brake inspection, Tire rotation.")
