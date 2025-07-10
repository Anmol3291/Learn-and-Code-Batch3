"""
Saved article-related CRUD operations for user article collections.
"""

import sqlite3
from datetime import datetime
import uuid
from typing import List, Tuple
from ..database.connection import get_db_connection
from .user_crud import get_user_by_username


def save_article(username: str, article_id: str) -> bool:
    """Save an article to user's collection."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Get user ID
        user = get_user_by_username(username)
        if not user:
            conn.close()
            return False
        
        user_id = user[0]
        
        # Check if article exists
        cur.execute("SELECT id FROM articles WHERE id = ?", (article_id,))
        if not cur.fetchone():
            conn.close()
            return False

        # Check if already saved
        cur.execute(
            "SELECT id FROM saved_articles WHERE user_id = ? AND article_id = ?",
            (user_id, article_id),
        )
        if cur.fetchone():
            conn.close()
            return False

        save_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO saved_articles (id, user_id, article_id, saved_at) VALUES (?, ?, ?, ?)",
            (save_id, user_id, article_id, datetime.now().isoformat()),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def get_saved_articles(username: str, page: int = 1, limit: int = 5) -> List[Tuple]:
    """Get user's saved articles with pagination."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    user = get_user_by_username(username)
    if not user:
        conn.close()
        return []
    
    user_id = user[0]
    offset = (page - 1) * limit
    
    cur.execute("""
        SELECT a.*, sa.saved_at 
        FROM articles a 
        JOIN saved_articles sa ON a.id = sa.article_id 
        WHERE sa.user_id = ? 
        ORDER BY sa.saved_at DESC 
        LIMIT ? OFFSET ?
    """, (user_id, limit, offset))
    
    articles = cur.fetchall()
    conn.close()
    return articles


def delete_saved_article(username: str, article_id: str) -> bool:
    """Remove article from user's saved collection."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user = get_user_by_username(username)
        if not user:
            conn.close()
            return False
        
        user_id = user[0]
        
        cur.execute(
            "DELETE FROM saved_articles WHERE user_id = ? AND article_id = ?",
            (user_id, article_id),
        )
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


def get_saved_articles_count(username: str) -> int:
    """Get total count of user's saved articles."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    user = get_user_by_username(username)
    if not user:
        conn.close()
        return 0
    
    user_id = user[0]
    
    cur.execute("SELECT COUNT(*) FROM saved_articles WHERE user_id = ?", (user_id,))
    count = cur.fetchone()[0]
    conn.close()
    return count


def is_article_saved(username: str, article_id: str) -> bool:
    """Check if article is saved by user."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    user = get_user_by_username(username)
    if not user:
        conn.close()
        return False
    
    user_id = user[0]
    
    cur.execute(
        "SELECT id FROM saved_articles WHERE user_id = ? AND article_id = ?",
        (user_id, article_id),
    )
    saved = cur.fetchone() is not None
    conn.close()
    return saved 