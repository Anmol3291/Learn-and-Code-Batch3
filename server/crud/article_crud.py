"""
Article-related CRUD operations for news article management.
"""

import sqlite3
from datetime import datetime
import uuid
import json
from typing import List, Tuple, Optional
from ..database.connection import get_db_connection


def get_articles_by_date(date: str, page: int = 1, limit: int = 5) -> List[Tuple]:
    """Get articles by specific date with pagination."""
    conn = get_db_connection()
    cur = conn.cursor()
    offset = (page - 1) * limit
    cur.execute(
        "SELECT * FROM articles WHERE published_date = ? ORDER BY created_at DESC LIMIT ? OFFSET ?", 
        (date, limit, offset)
    )
    articles = cur.fetchall()
    conn.close()
    return articles


def get_articles_by_date_range(start_date: str, end_date: str, page: int = 1, limit: int = 5) -> List[Tuple]:
    """Get articles within date range with pagination."""
    conn = get_db_connection()
    cur = conn.cursor()
    offset = (page - 1) * limit
    cur.execute(
        "SELECT * FROM articles WHERE published_date BETWEEN ? AND ? ORDER BY created_at DESC LIMIT ? OFFSET ?", 
        (start_date, end_date, limit, offset)
    )
    articles = cur.fetchall()
    conn.close()
    return articles


def get_articles_by_date_and_category(date: str, category: str, page: int = 1, limit: int = 5) -> List[Tuple]:
    """Get articles by date and category with pagination."""
    conn = get_db_connection()
    cur = conn.cursor()
    offset = (page - 1) * limit
    if category.lower() == "all":
        cur.execute(
            "SELECT * FROM articles WHERE published_date = ? ORDER BY created_at DESC LIMIT ? OFFSET ?", 
            (date, limit, offset)
        )
    else:
        cur.execute(
            "SELECT * FROM articles WHERE published_date = ? AND category = ? ORDER BY created_at DESC LIMIT ? OFFSET ?", 
            (date, category, limit, offset)
        )
    articles = cur.fetchall()
    conn.close()
    return articles


def get_articles_by_date_range_and_category(start_date: str, end_date: str, category: str, page: int = 1, limit: int = 5) -> List[Tuple]:
    """Get articles by date range and category with pagination."""
    conn = get_db_connection()
    cur = conn.cursor()
    offset = (page - 1) * limit
    if category.lower() == "all":
        cur.execute(
            "SELECT * FROM articles WHERE published_date BETWEEN ? AND ? ORDER BY created_at DESC LIMIT ? OFFSET ?", 
            (start_date, end_date, limit, offset)
        )
    else:
        cur.execute(
            "SELECT * FROM articles WHERE published_date BETWEEN ? AND ? AND category = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (start_date, end_date, category, limit, offset),
        )
    articles = cur.fetchall()
    conn.close()
    return articles


def check_article_exists(url: str) -> bool:
    """Check if article already exists by URL."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM articles WHERE url = ?", (url,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def add_article(title: str, content: str, source: str, url: str, category: Optional[str] = None, 
                keywords: Optional[List[str]] = None, published_date: Optional[str] = None) -> Optional[str]:
    """Add a new article to the database."""
    if not title or not content or not source or not url:
        return None
    
    if check_article_exists(url):
        return None
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        article_id = str(uuid.uuid4())
        keywords_json = json.dumps(keywords) if keywords else None
        pub_date = published_date or datetime.now().strftime("%Y-%m-%d")
        
        cur.execute("""
            INSERT INTO articles (id, title, content, source, url, category, keywords, published_date, created_at, likes, dislikes, vector_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, ?)
        """, (article_id, title, content, source, url, category, keywords_json, pub_date, datetime.now().isoformat(), None))
        
        conn.commit()
        return article_id
    except Exception:
        return None
    finally:
        conn.close()


def get_articles_count(date: Optional[str] = None, category: Optional[str] = None) -> int:
    """Get total count of articles with optional filters."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    if date and category:
        cur.execute("SELECT COUNT(*) FROM articles WHERE published_date = ? AND category = ?", (date, category))
    elif date:
        cur.execute("SELECT COUNT(*) FROM articles WHERE published_date = ?", (date,))
    elif category:
        cur.execute("SELECT COUNT(*) FROM articles WHERE category = ?", (category,))
    else:
        cur.execute("SELECT COUNT(*) FROM articles")
    
    count = cur.fetchone()[0]
    conn.close()
    return count


def get_articles_count_by_range(start_date: str, end_date: str, category: Optional[str] = None) -> int:
    """Get article count within date range with optional category filter."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    if category:
        cur.execute("SELECT COUNT(*) FROM articles WHERE published_date BETWEEN ? AND ? AND category = ?", 
                   (start_date, end_date, category))
    else:
        cur.execute("SELECT COUNT(*) FROM articles WHERE published_date BETWEEN ? AND ?", (start_date, end_date))
    
    count = cur.fetchone()[0]
    conn.close()
    return count


def get_article_by_id(article_id: str) -> Optional[Tuple]:
    """Get article by ID."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    article = cur.fetchone()
    conn.close()
    return article


def delete_article(article_id: str) -> bool:
    """Delete article by ID (admin functionality)."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM articles WHERE id = ?", (article_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


def update_article(article_id: str, title: str, content: str, category: str) -> bool:
    """Update article details (admin functionality)."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE articles SET title = ?, content = ?, category = ? WHERE id = ?",
            (title, content, category, article_id)
        )
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close() 