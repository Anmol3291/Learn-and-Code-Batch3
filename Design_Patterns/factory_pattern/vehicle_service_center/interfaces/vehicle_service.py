from abc import ABC, abstractmethod


class VehicleService(ABC):

    @abstractmethod
    def services(self):
        """Perform basic maintenance service for the vehicle."""
        pass
