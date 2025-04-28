from processors.OrderProcessor import OrderProcessor
from models.Customer import CustomerProcessor
from models.Product import Product


def main():
    customer_processor = CustomerProcessor()
    product_processor = Product()
    order_processor = OrderProcessor()

    customer_processor.add_customer(
        {
            "id": "CUST1",
            "name": "John Doe",
            "email": "john@example.com",
            "address": "123 Main St",
            "phone": "555-0123",
            "membership_level": "gold",
            "order_history": [],
        }
    )

    product_processor.add_product(
        {
            "id": "PROD1",
            "name": "Widget",
            "price": 99.99,
            "description": "A fantastic widget",
            "category": "gadgets",
            "stock": 100,
            "is_active": True,
        }
    )

    order_id = "ORD123"    
    order_details={
            "id": order_id,
            "customer_id": "CUST1",
            "items": [{"product_id": "PROD1", "quantity": 1, "price":99.99}],
            "total_amount": 99.99
        }

    result = order_processor.process_order(order_details)
    print(f"Order processing {'succeeded' if result else 'failed'}")


if __name__ == "__main__":
    main()
