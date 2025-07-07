"""
Scheduler module - imports all scheduler components.
"""

from .news_fetcher import NewsFetcher
from .article_processor import ArticleProcessor
from .notification_processor import NotificationProcessor
from .scheduler import NewsScheduler

# Create main scheduler instance
news_scheduler = NewsScheduler() 