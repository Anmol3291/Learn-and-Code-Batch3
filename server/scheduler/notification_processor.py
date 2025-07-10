"""
Notification processing functionality for user notifications.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
from ..services.email_service import EmailService
from ..crud.notification_crud import (
    get_user_notification_config, get_user_keywords, create_notification,
    mark_notification_email_sent
)
from ..database.connection import get_db_connection

logger = logging.getLogger(__name__)


class NotificationProcessor:
    """Handles processing and sending user notifications."""
    
    def __init__(self):
        self.email_service = EmailService()
    
    def process_notifications(self, newly_fetched_articles: Optional[List[Dict[str, Any]]] = None):
        """Process notifications for newly fetched articles."""
        if newly_fetched_articles is None:
            logger.info("No new articles provided, processing existing notifications")
            return
        
        if not newly_fetched_articles:
            logger.info("No new articles to process notifications for")
            return
        
        logger.info(f"Processing notifications for {len(newly_fetched_articles)} new articles")
        
        # Get all users
        users = self._get_all_users()
        if not users:
            logger.info("No users found for notifications")
            return
        
        # Process notifications for each user
        for user in users:
            try:
                self._process_user_notifications(user, newly_fetched_articles)
            except Exception as e:
                logger.error(f"Error processing notifications for user {user.get('username', 'Unknown')}: {e}")
    
    def _get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users from database."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email FROM users")
            users_data = cursor.fetchall()
            conn.close()
            
            users = []
            for user_data in users_data:
                users.append({
                    'id': user_data[0],
                    'username': user_data[1],
                    'email': user_data[2]
                })
            
            return users
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return []
    
    def _process_user_notifications(self, user: Dict[str, Any], newly_fetched_articles: List[Dict[str, Any]]):
        """Process notifications for a specific user."""
        username = user.get('username')
        user_id = user.get('id')
        email = user.get('email')
        
        if not username or not user_id:
            return
        
        # Get user preferences
        preferences = self._get_user_notification_preferences(username)
        
        # Find matching articles
        category_matches = []
        keyword_matches = []
        
        for article in newly_fetched_articles:
            # Check category matches
            if self._should_notify_category(username, article.get('category')):
                category_matches.append(article)
            
            # Check keyword matches
            if self._should_notify_keywords(username, article.get('keywords', [])):
                keyword_matches.append(article)
        
        # Create UI notifications
        if category_matches or keyword_matches:
            logger.info(f"🔔 User {username}: {len(category_matches)} category matches, {len(keyword_matches)} keyword matches")
            self._create_ui_notifications(user_id, category_matches, keyword_matches)
            
            # Send consolidated email
            if email:
                self._send_consolidated_email(email, username, category_matches, keyword_matches)
        else:
            logger.debug(f"📭 User {username}: No matching articles")
    
    def _get_user_notification_preferences(self, username: str) -> Dict[str, Any]:
        """Get user's notification preferences."""
        try:
            # Get category preferences
            category_config = get_user_notification_config(username)
            category_preferences = {cat: enabled for cat, enabled in category_config}
            
            # Get keyword preferences
            keywords = get_user_keywords(username)
            
            return {
                'categories': category_preferences,
                'keywords': keywords
            }
        except Exception as e:
            logger.error(f"Error getting preferences for {username}: {e}")
            return {'categories': {}, 'keywords': []}
    
    def _should_notify_category(self, username: str, category: str) -> bool:
        """Check if user should be notified for this category."""
        if not category:
            return False
        
        try:
            preferences = self._get_user_notification_preferences(username)
            return preferences.get('categories', {}).get(category, False)
        except Exception as e:
            logger.error(f"Error checking category notification for {username}: {e}")
            return False
    
    def _should_notify_keywords(self, username: str, article_keywords: List[str]) -> bool:
        """Check if user should be notified for these keywords."""
        if not article_keywords:
            return False
        
        try:
            preferences = self._get_user_notification_preferences(username)
            user_keywords = preferences.get('keywords', [])
            
            # Check if any article keywords match user keywords
            for article_keyword in article_keywords:
                if article_keyword.lower() in [kw.lower() for kw in user_keywords]:
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Error checking keyword notification for {username}: {e}")
            return False
    
    def _create_ui_notifications(self, user_id: str, category_matches: List[Dict[str, Any]], keyword_matches: List[Dict[str, Any]]):
        """Create UI notifications in database."""
        try:
            # Create notifications for category matches
            for article in category_matches:
                message = f"New {article.get('category', 'General')} article: {article.get('title', 'No title')}"
                create_notification(
                    user_id=user_id,
                    article_id=article.get('id', ''),
                    notification_type='category',
                    message=message
                )
            
            # Create notifications for keyword matches
            for article in keyword_matches:
                message = f"Article matching your keywords: {article.get('title', 'No title')}"
                create_notification(
                    user_id=user_id,
                    article_id=article.get('id', ''),
                    notification_type='keyword',
                    message=message
                )
                
        except Exception as e:
            logger.error(f"Error creating UI notifications: {e}")
    
    def _send_consolidated_email(self, email: str, username: str, category_matches: List[Dict[str, Any]], keyword_matches: List[Dict[str, Any]]):
        """Send consolidated email with all matching articles."""
        try:
            # Combine all matching articles
            all_matches = category_matches + keyword_matches
            
            # Remove duplicates based on article ID
            unique_matches = []
            seen_ids = set()
            for article in all_matches:
                article_id = article.get('id')
                if article_id and article_id not in seen_ids:
                    unique_matches.append(article)
                    seen_ids.add(article_id)
            
            if unique_matches:
                print(f"[EMAIL] Sending consolidated email to {email} with {len(unique_matches)} articles...")
                # Use the consolidated notification method from email service
                result = self.email_service.send_consolidated_notification(email, unique_matches)
                if result:
                    logger.info(f"📧 Consolidated email sent to {email} with {len(unique_matches)} articles")
                else:
                    logger.error(f"❌ Failed to send consolidated email to {email}")
                
        except Exception as e:
            logger.error(f"Error sending consolidated email to {email}: {e}") 