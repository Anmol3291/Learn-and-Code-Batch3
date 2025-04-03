from database.CustomerDatabase import CustomerDatabase

class CustomerValidator:
    customer_database=CustomerDatabase()

    def __init__(self):
        pass

    def is_valid_customer(self, customer_id:str):
        if(self.customer_database.get_details_by_id(id=customer_id)!="N/A"):
            return True
        else:
            print("Customer not found")
            return False
        

