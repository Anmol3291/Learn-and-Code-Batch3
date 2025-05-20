from vehicle_service_center.factory.vehicle_service_factory import VehicleServiceFactory


def main():
    """Main function to demonstrate the vehicle service factory implementation."""
    try:
        vehicle_type = input("Enter vehicle type (car, bike, truck): ")

        vehicle_object = VehicleServiceFactory.create_service(vehicle_type)

        print(vehicle_object.services())

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
