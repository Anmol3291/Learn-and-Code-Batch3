from database.ProductDatabase import ProductDatabase

class CartValidator:
    product_database=ProductDatabase()

    def __init__(self):
        pass

    def is_valid_cart(self, products: list):
        for item in products:
            product_id=item.get("product_id")
            product_quantity=item.get("quantity")
            if(not self.is_valid_product(product_id)):
               print(f"Product {product_id} not found")
               return False
            
            if(not self.is_item_in_stock(product_id, product_quantity)):
                print(f"Insufficient stock for product {product_id}")
                return False
        return True
                

    def is_item_in_stock(self, product_id: str, product_quantity: int):
        product_details=self.product_database.get_details_by_id(product_id)
        current_stock=product_details.get("stock")
        if(product_quantity<=current_stock):
            return True
        else:
            False

    def is_valid_product(self, product_id: str):
        product_details = self.product_database.get_details_by_id(product_id)
        if(product_details == "N/A"):
            return False
        else:
            return True