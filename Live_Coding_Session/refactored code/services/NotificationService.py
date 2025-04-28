import time
from abc import ABC, abstractmethod

class NotificationService(ABC):

    @abstractmethod
    def send_notification(self, message: str, email: str):
        pass

class CustomerNotificationService(NotificationService):

    def send_notification(self, message: str, email:str):
        
        try:
            print(f"Sending email to {email}: {message}")
            time.sleep(0.1)
        except Exception as e:
            print(f"Failed to send customer notification: {e}")


class AdminNotificationService(NotificationService):

    def send_notification(self, message: str, email: str= None):
        try:
            print(f"Admin notification: {message}")
            time.sleep(0.05)
        except Exception as e:
            print(f"Failed to send admin notification: {e}")


