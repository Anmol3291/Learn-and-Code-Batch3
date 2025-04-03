from validators.CustomerValidator import CustomerValidator
from validators.CartValidator import CartValidator

class OrderValidator:
    customer_validator = CustomerValidator()
    cart_validator= CartValidator()

    def __init__(self):
        pass

    def is_valid_order(self, order_details):
        customer_id=order_details.get("customer_id","N/A")
        products=order_details.get("items","N/A")
        if(not self.customer_validator.is_valid_customer(customer_id)
           and not self.cart_validator.is_valid_cart(products)):
            return False
        else:
            return True
