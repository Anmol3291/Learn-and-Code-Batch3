import datetime


class DateUtils:
    """Utility class for date operations"""

    @staticmethod
    def validate_date_format(date_string: str) -> bool:
        """Validate date format (YYYY-MM-DD)"""
        try:
            datetime.datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def get_current_date() -> str:
        """Get current date in YYYY-MM-DD format"""
        return datetime.datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def format_display_date(date_obj: datetime.datetime) -> str:
        """Format date for display"""
        return date_obj.strftime("%d-%b-%Y")

    @staticmethod
    def format_display_time(date_obj: datetime.datetime) -> str:
        """Format time for display"""
        return date_obj.strftime("%I:%M%p")
