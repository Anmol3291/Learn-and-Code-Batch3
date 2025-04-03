from database.BaseDatabase import BaseDatabase

class CustomerDatabase(BaseDatabase):
    __customers = {}

    def insert(self, details: dict):
        self.__customers[details["id"]] = details

    def get_details_by_id(self, id: str):
        return self.__customers.get(id,"N/A")
