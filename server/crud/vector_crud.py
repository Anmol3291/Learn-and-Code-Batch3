"""
Vector store-related CRUD operations for article embeddings.
"""

import sqlite3
from datetime import datetime
import uuid
from typing import Optional, Tuple
from ..database.connection import get_db_connection


def save_article_vector(article_id: str, vector_data: str) -> bool:
    """Save vector embedding for an article."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Check if vector already exists
        cur.execute("SELECT id FROM vector_store WHERE article_id = ?", (article_id,))
        if cur.fetchone():
            # Update existing vector
            cur.execute(
                "UPDATE vector_store SET vector_data = ?, created_at = ? WHERE article_id = ?",
                (vector_data, datetime.now().isoformat(), article_id)
            )
        else:
            # Create new vector
            vector_id = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO vector_store (id, article_id, vector_data, created_at) VALUES (?, ?, ?, ?)",
                (vector_id, article_id, vector_data, datetime.now().isoformat())
            )
        
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def get_article_vector(article_id: str) -> Optional[str]:
    """Get vector embedding for an article."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT vector_data FROM vector_store WHERE article_id = ?", (article_id,))
    result = cur.fetchone()
    conn.close()
    
    return result[0] if result else None


def delete_article_vector(article_id: str) -> bool:
    """Delete vector embedding for an article."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM vector_store WHERE article_id = ?", (article_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


def get_all_vectors() -> list[Tuple]:
    """Get all vector embeddings with article IDs."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT article_id, vector_data FROM vector_store")
    vectors = cur.fetchall()
    conn.close()
    
    return vectors


def update_article_vector_id(article_id: str, vector_id: str) -> bool:
    """Update article's vector_id reference."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE articles SET vector_id = ? WHERE id = ?",
            (vector_id, article_id)
        )
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close() 