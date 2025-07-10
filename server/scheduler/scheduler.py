"""
Main scheduler that coordinates news fetching, processing, and notifications.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from .news_fetcher import NewsFetcher
from .article_processor import ArticleProcessor
from .notification_processor import NotificationProcessor

logger = logging.getLogger(__name__)


class NewsScheduler:
    """Main scheduler that coordinates news fetching, processing, and notifications."""

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.news_fetcher = NewsFetcher()
        self.article_processor = ArticleProcessor()
        self.notification_processor = NotificationProcessor()

        self.is_running = False
        self.last_fetch_time = None
        self.last_notification_time = None

    def start(self):
        """Start the scheduler with configured jobs."""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return

        try:
            # Schedule news fetching every hour
            self.scheduler.add_job(
                func=self._fetch_and_process_news,
                trigger=IntervalTrigger(hours=1),
                id="news_fetch_job",
                name="Fetch and Process News",
                replace_existing=True,
            )

            # Schedule notification processing every 30 minutes
            self.scheduler.add_job(
                func=self._process_notifications,
                trigger=IntervalTrigger(minutes=30),
                id="notification_job",
                name="Process Notifications",
                replace_existing=True,
            )

            # Start the scheduler
            self.scheduler.start()
            self.is_running = True

            logger.info("News scheduler started successfully")
            logger.info("Jobs scheduled:")
            logger.info("  - News fetching: Every 1 hour")
            logger.info("  - Notification processing: Every 30 minutes")

            # Immediately fetch news and send notifications on startup
            self._fetch_and_process_news()

        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
            raise

    def stop(self):
        """Stop the scheduler."""
        if not self.is_running:
            logger.warning("Scheduler is not running")
            return

        try:
            self.scheduler.shutdown(wait=False)
            self.is_running = False
            logger.info("News scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")

    def _fetch_and_process_news(self):
        """Fetch news from APIs and process articles."""
        logger.info("Starting scheduled news fetch and processing...")

        try:
            # Fetch news from external APIs
            articles = self.news_fetcher.fetch_news()

            if not articles:
                logger.warning("No articles fetched from external APIs")
                return

            # Process and store articles
            processing_result = self.article_processor.process_articles(articles)

            # Update last fetch time
            self.last_fetch_time = datetime.now()

            logger.info(f"News fetch and processing completed: {processing_result}")

            # Trigger notification processing after news fetch with the newly fetched articles
            self.notification_processor.process_notifications(articles)

        except Exception as e:
            logger.error(f"Error in news fetch and processing: {e}")

    def _process_notifications(self):
        """Process notifications for users."""
        logger.info("Starting scheduled notification processing...")

        try:
            # Process notifications without new articles (for scheduled processing)
            self.notification_processor.process_notifications()

            # Update last notification time
            self.last_notification_time = datetime.now()

            logger.info("Notification processing completed")

        except Exception as e:
            logger.error(f"Error in notification processing: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get current scheduler status."""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append(
                {
                    "id": job.id,
                    "name": job.name,
                    "next_run": (
                        job.next_run_time.isoformat() if job.next_run_time else None
                    ),
                    "trigger": str(job.trigger),
                }
            )

        return {
            "is_running": self.is_running,
            "jobs": jobs,
            "last_fetch_time": (
                self.last_fetch_time.isoformat() if self.last_fetch_time else None
            ),
            "last_notification_time": (
                self.last_notification_time.isoformat()
                if self.last_notification_time
                else None
            ),
            "processing_stats": self.article_processor.get_processing_stats(),
        }

    def trigger_manual_fetch(self) -> Dict[str, Any]:
        """Manually trigger news fetching and processing."""
        logger.info("Manual news fetch triggered")

        try:
            # Fetch news from external APIs
            articles = self.news_fetcher.fetch_news()

            if not articles:
                return {
                    "success": False,
                    "message": "No articles fetched from external APIs",
                    "articles_fetched": 0,
                    "articles_processed": 0,
                    "notifications_sent": 0,
                }

            # Process and store articles
            processing_result = self.article_processor.process_articles(articles)

            # Update last fetch time
            self.last_fetch_time = datetime.now()

            # Trigger notification processing with the newly fetched articles
            notification_result = self.notification_processor.process_notifications(
                articles
            )

            return {
                "success": True,
                "message": "Manual news fetch completed successfully",
                "articles_fetched": len(articles),
                "articles_processed": processing_result["processed"],
                "articles_skipped": processing_result["skipped"],
                "notifications_sent": notification_result.get("sent", 0),
                "notifications_skipped": notification_result.get("skipped", 0),
            }

        except Exception as e:
            logger.error(f"Error in manual news fetch: {e}")
            return {
                "success": False,
                "message": f"Error in manual news fetch: {str(e)}",
                "articles_fetched": 0,
                "articles_processed": 0,
                "notifications_sent": 0,
            }

    def trigger_manual_notifications(self) -> Dict[str, Any]:
        """Manually trigger notification processing."""
        logger.info("Manual notification processing triggered")

        try:
            # Process notifications
            notification_result = self.notification_processor.process_notifications()

            # Update last notification time
            self.last_notification_time = datetime.now()

            return {
                "success": True,
                "message": "Manual notification processing completed successfully",
                "notifications_sent": notification_result.get("sent", 0),
                "notifications_skipped": notification_result.get("skipped", 0),
            }

        except Exception as e:
            logger.error(f"Error in manual notification processing: {e}")
            return {
                "success": False,
                "message": f"Error in manual notification processing: {str(e)}",
                "notifications_sent": 0,
                "notifications_skipped": 0,
            }

    def update_schedule(
        self, news_interval_hours: int = 1, notification_interval_minutes: int = 30
    ):
        """Update scheduler intervals."""
        if not self.is_running:
            logger.warning("Cannot update schedule - scheduler is not running")
            return False

        try:
            # Remove existing jobs
            self.scheduler.remove_job("news_fetch_job")
            self.scheduler.remove_job("notification_job")

            # Add updated jobs
            self.scheduler.add_job(
                func=self._fetch_and_process_news,
                trigger=IntervalTrigger(hours=news_interval_hours),
                id="news_fetch_job",
                name="Fetch and Process News",
                replace_existing=True,
            )

            self.scheduler.add_job(
                func=self._process_notifications,
                trigger=IntervalTrigger(minutes=notification_interval_minutes),
                id="notification_job",
                name="Process Notifications",
                replace_existing=True,
            )

            logger.info(
                f"Schedule updated - News: {news_interval_hours}h, Notifications: {notification_interval_minutes}m"
            )
            return True

        except Exception as e:
            logger.error(f"Error updating schedule: {e}")
            return False


news_scheduler = NewsScheduler()
