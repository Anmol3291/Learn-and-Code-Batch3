class Config:
    """Application configuration"""

    BASE_URL = "http://localhost:8000"
    SECRET_KEY = "your-very-secret-key"
    ALGORITHM = "HS256"

    ENDPOINTS = {
        "signup": "/signup",
        "login": "/login",
        "servers": "/servers",
        "server_details": "/server-details",
        "update_server": "/update-server",
        "add_category": "/add-category",
        "get_categories": "/get-categories",
        "articles_today": "/articles/today",
        "articles_date_range": "/articles/date-range",
        "save_article": "/save-article",
        "saved_articles": "/saved-articles",
    }

    CATEGORIES = {
        "1": "All",
        "2": "Business",
        "3": "Entertainment",
        "4": "Sports",
        "5": "Technology",
    }
