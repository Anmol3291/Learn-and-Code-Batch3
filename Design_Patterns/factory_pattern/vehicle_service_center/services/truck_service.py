from vehicle_service_center.interfaces.vehicle_service import VehicleService


class TruckService(VehicleService):
    """Implementation of vehicle service operations for trucks."""

    def service(self):
        """Perform Heavy-duty engine diagnostics and cargo inspection service for truck."""
        print("Truck Service: Heavy-duty engine diagnostics, Cargo inspection.")
