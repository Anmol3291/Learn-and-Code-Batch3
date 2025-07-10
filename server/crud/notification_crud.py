"""
Notification-related CRUD operations for user notifications and preferences.
"""

import sqlite3
from datetime import datetime
import uuid
import json
from typing import List, Tuple, Optional
from ..database.connection import get_db_connection
from .user_crud import get_user_by_username


def get_user_notifications(username: str) -> List[Tuple]:
    """Get all notifications for a user."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    user = get_user_by_username(username)
    if not user:
        conn.close()
        return []
    
    user_id = user[0]
    
    cur.execute("""
        SELECT n.*, a.title, a.url 
        FROM notifications n 
        LEFT JOIN articles a ON n.article_id = a.id 
        WHERE n.user_id = ? 
        ORDER BY n.sent_at DESC
    """, (user_id,))
    
    notifications = cur.fetchall()
    conn.close()
    return notifications


def get_user_notification_config(username: str) -> List[Tuple]:
    """Get user's notification preferences by category."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    user = get_user_by_username(username)
    if not user:
        conn.close()
        return []
    
    user_id = user[0]
    
    cur.execute("""
        SELECT category, enabled 
        FROM user_notifications 
        WHERE user_id = ?
    """, (user_id,))
    
    config = cur.fetchall()
    conn.close()
    return config


def update_user_notification_config(username: str, category: str, enabled: bool) -> bool:
    """Update user's notification preference for a category."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user = get_user_by_username(username)
        if not user:
            conn.close()
            return False
        
        user_id = user[0]
        
        # Check if config exists
        cur.execute(
            "SELECT id FROM user_notifications WHERE user_id = ? AND category = ?",
            (user_id, category)
        )
        
        if cur.fetchone():
            # Update existing config
            cur.execute(
                "UPDATE user_notifications SET enabled = ? WHERE user_id = ? AND category = ?",
                (enabled, user_id, category)
            )
        else:
            # Create new config
            config_id = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO user_notifications (id, user_id, category, enabled, created_at) VALUES (?, ?, ?, ?, ?)",
                (config_id, user_id, category, enabled, datetime.now().isoformat())
            )
        
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def get_user_keywords(username: str) -> List[str]:
    """Get user's keyword preferences."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    user = get_user_by_username(username)
    if not user:
        conn.close()
        return []
    
    user_id = user[0]
    
    cur.execute("SELECT keywords FROM user_keywords WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    
    if result and result[0]:
        return json.loads(result[0])
    return []


def update_user_keywords(username: str, keywords: List[str]) -> bool:
    """Update user's keyword preferences."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user = get_user_by_username(username)
        if not user:
            conn.close()
            return False
        
        user_id = user[0]
        keywords_json = json.dumps(keywords)
        
        # Check if keywords config exists
        cur.execute("SELECT id FROM user_keywords WHERE user_id = ?", (user_id,))
        
        if cur.fetchone():
            # Update existing config
            cur.execute(
                "UPDATE user_keywords SET keywords = ? WHERE user_id = ?",
                (keywords_json, user_id)
            )
        else:
            # Create new config
            config_id = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO user_keywords (id, user_id, keywords, created_at) VALUES (?, ?, ?, ?)",
                (config_id, user_id, keywords_json, datetime.now().isoformat())
            )
        
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def create_notification(user_id: str, article_id: str, notification_type: str, message: str) -> Optional[str]:
    """Create a new notification for a user."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        notification_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO notifications (id, user_id, article_id, notification_type, message, sent_at) VALUES (?, ?, ?, ?, ?, ?)",
            (notification_id, user_id, article_id, notification_type, message, datetime.now().isoformat())
        )
        conn.commit()
        return notification_id
    except Exception:
        return None
    finally:
        conn.close()


def mark_notification_email_sent(notification_id: str) -> bool:
    """Mark notification as email sent."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE notifications SET email_sent = 1 WHERE id = ?",
            (notification_id,)
        )
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


def delete_notification(notification_id: str) -> bool:
    """Delete a specific notification."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


def delete_user_notifications(username: str) -> bool:
    """Delete all notifications for a user."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user = get_user_by_username(username)
        if not user:
            conn.close()
            return False
        
        user_id = user[0]
        cur.execute("DELETE FROM notifications WHERE user_id = ?", (user_id,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def get_users_for_category_notification(category: str) -> List[Tuple]:
    """Get users who have notifications enabled for a category."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT u.id, u.username, u.email 
        FROM users u 
        JOIN user_notifications un ON u.id = un.user_id 
        WHERE un.category = ? AND un.enabled = 1
    """, (category,))
    
    users = cur.fetchall()
    conn.close()
    return users


def get_users_for_keyword_notification() -> List[Tuple]:
    """Get users who have keyword notifications configured."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT u.id, u.username, u.email, uk.keywords 
        FROM users u 
        JOIN user_keywords uk ON u.id = uk.user_id 
        WHERE uk.keywords IS NOT NULL AND uk.keywords != '[]'
    """)
    
    users = cur.fetchall()
    conn.close()
    return users 