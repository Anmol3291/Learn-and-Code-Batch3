"""
Search-related CRUD operations for article search functionality.
"""

import sqlite3
from typing import List, Tuple, Optional
from ..database.connection import get_db_connection


def search_articles(query: str, category: Optional[str] = None, date_from: Optional[str] = None, 
                   date_to: Optional[str] = None, page: int = 1, limit: int = 5) -> List[Tuple]:
    """Search articles with filters and pagination."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    offset = (page - 1) * limit
    conditions = ["(title LIKE ? OR content LIKE ?)"]
    params = [f"%{query}%", f"%{query}%"]
    
    if category and category.lower() != "all":
        conditions.append("category = ?")
        params.append(category)
    
    if date_from:
        conditions.append("published_date >= ?")
        params.append(date_from)
    
    if date_to:
        conditions.append("published_date <= ?")
        params.append(date_to)
    
    where_clause = " AND ".join(conditions)
    params.extend([limit, offset])
    
    sql = f"""
        SELECT * FROM articles 
        WHERE {where_clause}
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    """
    
    cur.execute(sql, params)
    articles = cur.fetchall()
    conn.close()
    return articles


def search_articles_count(query: str, category: Optional[str] = None, date_from: Optional[str] = None, 
                         date_to: Optional[str] = None) -> int:
    """Get total count of search results."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    conditions = ["(title LIKE ? OR content LIKE ?)"]
    params = [f"%{query}%", f"%{query}%"]
    
    if category and category.lower() != "all":
        conditions.append("category = ?")
        params.append(category)
    
    if date_from:
        conditions.append("published_date >= ?")
        params.append(date_from)
    
    if date_to:
        conditions.append("published_date <= ?")
        params.append(date_to)
    
    where_clause = " AND ".join(conditions)
    
    sql = f"SELECT COUNT(*) FROM articles WHERE {where_clause}"
    
    cur.execute(sql, params)
    count = cur.fetchone()[0]
    conn.close()
    return count


def search_by_keywords(keywords: List[str], page: int = 1, limit: int = 5) -> List[Tuple]:
    """Search articles by keywords in title, content, or keywords field."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    offset = (page - 1) * limit
    conditions = []
    params = []
    
    for keyword in keywords:
        conditions.append("(title LIKE ? OR content LIKE ? OR keywords LIKE ?)")
        params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
    
    where_clause = " OR ".join(conditions)
    params.extend([limit, offset])
    
    sql = f"""
        SELECT * FROM articles 
        WHERE {where_clause}
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    """
    
    cur.execute(sql, params)
    articles = cur.fetchall()
    conn.close()
    return articles


def search_by_keywords_count(keywords: List[str]) -> int:
    """Get total count of articles matching keywords."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    conditions = []
    params = []
    
    for keyword in keywords:
        conditions.append("(title LIKE ? OR content LIKE ? OR keywords LIKE ?)")
        params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
    
    where_clause = " OR ".join(conditions)
    
    sql = f"SELECT COUNT(*) FROM articles WHERE {where_clause}"
    
    cur.execute(sql, params)
    count = cur.fetchone()[0]
    conn.close()
    return count


def get_popular_articles(days: int = 7, limit: int = 10) -> List[Tuple]:
    """Get most popular articles based on likes in recent days."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql = """
        SELECT * FROM articles 
        WHERE published_date >= date('now', '-{} days')
        ORDER BY likes DESC, created_at DESC 
        LIMIT ?
    """.format(days)
    
    cur.execute(sql, (limit,))
    articles = cur.fetchall()
    conn.close()
    return articles


def get_recent_articles(limit: int = 10) -> List[Tuple]:
    """Get most recent articles."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT * FROM articles 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (limit,))
    
    articles = cur.fetchall()
    conn.close()
    return articles 