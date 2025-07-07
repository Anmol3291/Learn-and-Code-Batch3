"""
Reaction-related CRUD operations for article likes and dislikes.
"""

import sqlite3
from datetime import datetime
import uuid
from typing import List, Tuple, Optional
from ..database.connection import get_db_connection
from .user_crud import get_user_by_username


def like_article(username: str, article_id: str) -> bool:
    """Like an article and update article stats."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
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
        
        # Check if user already liked
        cur.execute(
            "SELECT id FROM article_reactions WHERE user_id = ? AND article_id = ? AND reaction_type = 'like'",
            (user_id, article_id)
        )
        if cur.fetchone():
            conn.close()
            return False
        
        # Remove any existing dislike
        cur.execute(
            "DELETE FROM article_reactions WHERE user_id = ? AND article_id = ? AND reaction_type = 'dislike'",
            (user_id, article_id)
        )
        
        # Add like
        reaction_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO article_reactions (id, user_id, article_id, reaction_type, created_at) VALUES (?, ?, ?, 'like', ?)",
            (reaction_id, user_id, article_id, datetime.now().isoformat())
        )
        
        # Update article stats
        cur.execute(
            "UPDATE articles SET likes = likes + 1 WHERE id = ?",
            (article_id,)
        )
        
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def dislike_article(username: str, article_id: str) -> bool:
    """Dislike an article and update article stats."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
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
        
        # Check if user already disliked
        cur.execute(
            "SELECT id FROM article_reactions WHERE user_id = ? AND article_id = ? AND reaction_type = 'dislike'",
            (user_id, article_id)
        )
        if cur.fetchone():
            conn.close()
            return False
        
        # Remove any existing like
        cur.execute(
            "DELETE FROM article_reactions WHERE user_id = ? AND article_id = ? AND reaction_type = 'like'",
            (user_id, article_id)
        )
        
        # Add dislike
        reaction_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO article_reactions (id, user_id, article_id, reaction_type, created_at) VALUES (?, ?, ?, 'dislike', ?)",
            (reaction_id, user_id, article_id, datetime.now().isoformat())
        )
        
        # Update article stats
        cur.execute(
            "UPDATE articles SET dislikes = dislikes + 1 WHERE id = ?",
            (article_id,)
        )
        
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def unlike_article(username: str, article_id: str) -> bool:
    """Remove like from article and update stats."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user = get_user_by_username(username)
        if not user:
            conn.close()
            return False
        
        user_id = user[0]
        
        # Remove like
        cur.execute(
            "DELETE FROM article_reactions WHERE user_id = ? AND article_id = ? AND reaction_type = 'like'",
            (user_id, article_id)
        )
        
        if cur.rowcount > 0:
            # Update article stats
            cur.execute(
                "UPDATE articles SET likes = likes - 1 WHERE id = ?",
                (article_id,)
            )
            conn.commit()
            return True
        
        return False
    except Exception:
        return False
    finally:
        conn.close()


def remove_dislike(username: str, article_id: str) -> bool:
    """Remove dislike from article and update stats."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user = get_user_by_username(username)
        if not user:
            conn.close()
            return False
        
        user_id = user[0]
        
        # Remove dislike
        cur.execute(
            "DELETE FROM article_reactions WHERE user_id = ? AND article_id = ? AND reaction_type = 'dislike'",
            (user_id, article_id)
        )
        
        if cur.rowcount > 0:
            # Update article stats
            cur.execute(
                "UPDATE articles SET dislikes = dislikes - 1 WHERE id = ?",
                (article_id,)
            )
            conn.commit()
            return True
        
        return False
    except Exception:
        return False
    finally:
        conn.close()


def get_liked_articles(username: str, page: int = 1, limit: int = 5) -> List[Tuple]:
    """Get articles liked by user with pagination."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    user = get_user_by_username(username)
    if not user:
        conn.close()
        return []
    
    user_id = user[0]
    offset = (page - 1) * limit
    
    cur.execute("""
        SELECT a.*, ar.created_at as reaction_date
        FROM articles a 
        JOIN article_reactions ar ON a.id = ar.article_id 
        WHERE ar.user_id = ? AND ar.reaction_type = 'like'
        ORDER BY ar.created_at DESC 
        LIMIT ? OFFSET ?
    """, (user_id, limit, offset))
    
    articles = cur.fetchall()
    conn.close()
    return articles


def get_disliked_articles(username: str, page: int = 1, limit: int = 5) -> List[Tuple]:
    """Get articles disliked by user with pagination."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    user = get_user_by_username(username)
    if not user:
        conn.close()
        return []
    
    user_id = user[0]
    offset = (page - 1) * limit
    
    cur.execute("""
        SELECT a.*, ar.created_at as reaction_date
        FROM articles a 
        JOIN article_reactions ar ON a.id = ar.article_id 
        WHERE ar.user_id = ? AND ar.reaction_type = 'dislike'
        ORDER BY ar.created_at DESC 
        LIMIT ? OFFSET ?
    """, (user_id, limit, offset))
    
    articles = cur.fetchall()
    conn.close()
    return articles


def get_liked_articles_count(username: str) -> int:
    """Get total count of articles liked by user."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    user = get_user_by_username(username)
    if not user:
        conn.close()
        return 0
    
    user_id = user[0]
    
    cur.execute(
        "SELECT COUNT(*) FROM article_reactions WHERE user_id = ? AND reaction_type = 'like'", 
        (user_id,)
    )
    count = cur.fetchone()[0]
    conn.close()
    return count


def get_disliked_articles_count(username: str) -> int:
    """Get total count of articles disliked by user."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    user = get_user_by_username(username)
    if not user:
        conn.close()
        return 0
    
    user_id = user[0]
    
    cur.execute(
        "SELECT COUNT(*) FROM article_reactions WHERE user_id = ? AND reaction_type = 'dislike'", 
        (user_id,)
    )
    count = cur.fetchone()[0]
    conn.close()
    return count


def get_article_reaction_stats(article_id: str) -> Tuple[int, int]:
    """Get like and dislike counts for an article."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT likes, dislikes FROM articles WHERE id = ?", (article_id,))
    result = cur.fetchone()
    conn.close()
    
    if result:
        return result[0], result[1]
    return 0, 0


def get_user_reaction(username: str, article_id: str) -> Optional[str]:
    """Get user's reaction to an article (like, dislike, or None)."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    user = get_user_by_username(username)
    if not user:
        conn.close()
        return None
    
    user_id = user[0]
    
    cur.execute(
        "SELECT reaction_type FROM article_reactions WHERE user_id = ? AND article_id = ?",
        (user_id, article_id)
    )
    result = cur.fetchone()
    conn.close()
    
    return result[0] if result else None 