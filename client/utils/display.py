from datetime import datetime
from typing import List, Optional


class DisplayUtils:
    """Utility class for formatting and displaying data in the application."""
    
    # Display constants
    DEFAULT_TRUNCATE_LENGTH = 150
    TRUNCATE_SUFFIX = "..."
    SEPARATOR_LENGTH = 80
    SHORT_SEPARATOR_LENGTH = 60
    MENU_SEPARATOR_LENGTH = 50
    
    # Date formats
    DATE_FORMATS = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
    DISPLAY_DATE_FORMAT = "%d-%b-%Y"
    DISPLAY_DATETIME_FORMAT = "%d-%b-%Y %I:%M%p"
    
    @staticmethod
    def format_date(date_str: str) -> str:
        """Format date string to a readable format."""
        try:
            if isinstance(date_str, str):
                for fmt in DisplayUtils.DATE_FORMATS:
                    try:
                        dt = datetime.strptime(date_str, fmt)
                        return dt.strftime(DisplayUtils.DISPLAY_DATE_FORMAT)
                    except ValueError:
                        continue
            return date_str
        except Exception:
            return date_str
    
    @staticmethod
    def format_datetime(datetime_str: str) -> str:
        """Format datetime string to a readable format."""
        try:
            if isinstance(datetime_str, str):
                for fmt in DisplayUtils.DATE_FORMATS:
                    try:
                        dt = datetime.strptime(datetime_str, fmt)
                        return dt.strftime(DisplayUtils.DISPLAY_DATETIME_FORMAT)
                    except ValueError:
                        continue
            return datetime_str
        except Exception:
            return datetime_str
    
    @staticmethod
    def truncate_text(text: str, max_length: int = None, suffix: str = None) -> str:
        """Truncate text to specified length with suffix."""
        if max_length is None:
            max_length = DisplayUtils.DEFAULT_TRUNCATE_LENGTH
        if suffix is None:
            suffix = DisplayUtils.TRUNCATE_SUFFIX
            
        if not text:
            return ""
        
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def format_article_display(article: dict) -> str:
        """Format article data for display."""
        if not article:
            return "Invalid article data"
        
        article_id = article.get('id', 'N/A')
        title = article.get('title', 'No title')
        content = article.get('content', 'No content')
        source = article.get('source', 'Unknown')
        url = article.get('url', 'No URL')
        category = article.get('category')
        
        display = f"\nArticle ID: {article_id}\n"
        display += f"Title: {title}\n"
        display += f"Content: {DisplayUtils.truncate_text(content, 150)}...\n"
        display += f"Source: {source}\n"
        display += f"URL: {url}\n"
        
        if category:
            display += f"Category: {category}\n"
        
        display += "-" * DisplayUtils.SEPARATOR_LENGTH
        return display
    
    @staticmethod
    def get_pagination_info(current_page: int, total_pages: int, 
                           total_items: int, items_per_page: int) -> str:
        """Generate pagination information string."""
        start_item = (current_page - 1) * items_per_page + 1
        end_item = min(current_page * items_per_page, total_items)
        
        return f"Showing {start_item}-{end_item} of {total_items} items (Page {current_page} of {total_pages})"
    
    @staticmethod
    def format_notification_display(notification: dict) -> str:
        """Format notification data for display."""
        if not notification:
            return "Invalid notification data"
        
        notification_type = notification.get('notification_type', 'Unknown')
        message = notification.get('message', 'No message')
        sent_at = notification.get('sent_at', 'Unknown time')
        email_sent = notification.get('email_sent', False)
        
        display = f"\n{notification_type.upper()}\n"
        display += f"   {message}\n"
        display += f"   Sent: {DisplayUtils.format_datetime(sent_at)}\n"
        
        if email_sent:
            display += "   Email sent\n"
        
        display += "-" * DisplayUtils.SHORT_SEPARATOR_LENGTH
        return display
    
    @staticmethod
    def get_category_display_name(category: str) -> str:
        """Get formatted category display name."""
        if not category:
            return "All Categories"
        
        return " ".join(word.capitalize() for word in category.split())
    
    @staticmethod
    def format_keywords_display(keywords: List[str]) -> str:
        """Format keywords list for display."""
        if not keywords:
            return "No keywords configured"
        
        return ", ".join(keywords)
    
    @staticmethod
    def get_current_datetime() -> str:
        """Get current datetime in application format."""
        return datetime.now().strftime(DisplayUtils.DISPLAY_DATETIME_FORMAT)
    
    @staticmethod
    def get_menu_separator() -> str:
        """Get consistent menu separator."""
        return "-" * DisplayUtils.MENU_SEPARATOR_LENGTH
    
    @staticmethod
    def format_success_message(message: str) -> str:
        """Format success message."""
        return f"SUCCESS: {message}"
    
    @staticmethod
    def format_error_message(message: str) -> str:
        """Format error message."""
        return f"ERROR: {message}"
    
    @staticmethod
    def format_warning_message(message: str) -> str:
        """Format warning message."""
        return f"WARNING: {message}"
    
    @staticmethod
    def format_info_message(message: str) -> str:
        """Format info message."""
        return f"INFO: {message}" 