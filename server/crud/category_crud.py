"""
Category-related CRUD operations for article categorization.
"""

import sqlite3
from datetime import datetime
import uuid
from typing import List, Tuple
from ..database.connection import get_db_connection


def add_category(name: str) -> bool:
    """Add a new article category."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cat_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO categories (id, name, created_at) VALUES (?, ?, ?)", 
            (cat_id, name, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_categories() -> List[Tuple]:
    """Get all available categories."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at FROM categories ORDER BY name")
    categories = cur.fetchall()
    conn.close()
    return categories


def get_category_by_name(name: str) -> Tuple:
    """Get category by name."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at FROM categories WHERE name = ?", (name,))
    category = cur.fetchone()
    conn.close()
    return category


def delete_category(category_id: str) -> bool:
    """Delete a category (admin functionality)."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


def update_category(category_id: str, name: str) -> bool:
    """Update category name (admin functionality)."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE categories SET name = ? WHERE id = ?", (name, category_id)
        )
        conn.commit()
        return cur.rowcount > 0
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close() 