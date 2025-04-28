from database.CustomerDatabase import CustomerDatabase


class CustomerProcessor:
    customer_database_obj = CustomerDatabase()

    def add_customer(self, customer):
        if not customer.get("id") or not customer.get("email"):
            return False
        self.customer_database_obj.insert(customer)
        return True
    
    def is_customer_present(self, customer_id):
        if(self.customer_database_obj.get_customer_details(customer_id) == "N/A"):
            return False
        return

