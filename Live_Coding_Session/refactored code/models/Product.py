from database.ProductDatabase import ProductDatabase


class Product:
    product_database_obj = ProductDatabase()
    def __init__(self):
        pass

    def add_product(self, product):
        if not product.get("id") or product.get("price", 0) < 0:
            return False
        self.product_database_obj.insert(product)
        return True
