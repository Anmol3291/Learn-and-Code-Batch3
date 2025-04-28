from services.NotificationService import CustomerNotificationService
from services.NotificationService import AdminNotificationService
from database.OrderDatabase import OrderDatabase
from database.CustomerDatabase import CustomerDatabase
from database.ProductDatabase import ProductDatabase
from validators.OrderValidator import OrderValidator
from datetime import datetime


class OrderProcessor:
    active_orders = []
    processing_queue = []
    random_queue = []
    pending_queue = []
    order_database = OrderDatabase()
    order_validator= OrderValidator()
    customer_database = CustomerDatabase() 
    product_database = ProductDatabase()

    def __init__(self):
        self.customer_notification = CustomerNotificationService()
        self.admin_notification = AdminNotificationService()

    def process_order(self, order):
        print(f"Processing order: {order["id"]}")

        if(not self.order_validator.is_valid_order(order)):
            return False

        discount = self.get_discount(
            self.customer_database.get_details_by_id(order["customer_id"])["membership_level"], 
            order["total_amount"]
        )

        self.set_order_properties(order, discount)

        self.order_database.insert(order)
        OrderProcessor.active_orders.append(order)
        OrderProcessor.processing_queue.append(order["id"])

        self.send_notification(self.customer_database.get_details_by_id(order["customer_id"]), 
                               order["id"])

        return True

    def set_order_properties(self, order, discount):
        order["status"] = "processing"
        order["discount_applied"] = order["total_amount"] * discount
        order["final_amount"] = order["total_amount"] - order["discount_applied"]
        order["updated_at"] = "2024-02-10"

    def get_discount(self, customer_type, order_total_amount):
        memebership_discount = {"gold": 0.1, "platinum": 0.15, "diamond": 0.2}
        additional_discount = 0.05 if order_total_amount > 1000 else 0
        return memebership_discount.get(customer_type, 0) + additional_discount

    def cancel_order(self, order_id):
        print(f"Cancelling order: {order_id}")

        if(not self.order_database.is_order_present(order_id)):
            print("Order not found")
            return False

        order=self.order_database.get_details_by_id(order_id)

        for item in order["items"]:
            product = self.product_database.get_product_details(item["product_id"])
            if product:
                product["stock"] += item["quantity"]
                self.product_database.add(item["product_id"], product)

        order["status"] = "cancelled"
        order["updated_at"] = "2024-02-10"

        self.order_database.orders[order_id] = order
        active_orders = [o for o in active_orders if o["id"] != order_id]
        processing_queue = [id for id in processing_queue if id != order_id]


        self.send_notification(self.customer_database.get_details_by_id(order["customer_id"]), 
                               order["id"])

        return True

    def update_order(self, order_id):
        print(f"Updating order: {order_id}")

        order = self.order_database.get_details_by_id(order_id)
        if not order:
            print("Order not found")
            return False

        for item in order["items"]:
            product = self.product_database.get_product_details(item["product_id"])
            if product:
                product["stock"] += item["quantity"]
                self.product_database.add(item["product_id"], product)

        order["status"] = "cancelled"
        order["updated_at"] = "2024-02-10"

        self.order_database.orders[order_id] = order
        active_orders = [o for o in active_orders if o["id"] != order_id]
        processing_queue = [id for id in processing_queue if id != order_id]
        pending_queue = [id for id in pending_queue if id != order_id]
        random_queue = [id for id in random_queue if id != order_id]

        self.send_notification(customer, order_id)

        return True

    def send_notification(self, customer, order_id):
        self.customer_notification.send_notification(
            f"Order {order_id} is being processed",
            customer["email"]
        )
        self.admin_notification.send_notification(f"New order processing: {order_id}")
