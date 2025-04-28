from database.BaseDatabase import BaseDatabase

class OrderDatabase(BaseDatabase):
    __orders = {}

    def insert(self, details: dict):
        self.__orders[details["id"]] = details

    def get_details_by_id(self, id: str):
        return self.__orders.get(id,"N/A")
    
    def is_order_present(self, order_id: str): 
        if(order_id in self.__orders):
            return True
        else:
            False