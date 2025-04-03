from abc import ABC, abstractmethod

class BaseDatabase:

    @abstractmethod
    def insert(self, details: dict):
        pass

    @abstractmethod
    def get_details_by_id(self, id: str):
        pass
    
