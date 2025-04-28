from database.BaseDatabase import BaseDatabase

class ProductDatabase(BaseDatabase):
    __products = {}

    def insert(self, details):
        self.__products[details["id"]] = details

    def get_details_by_id(self, id: str):
        return self.__products.get(id,"N/A")
    

