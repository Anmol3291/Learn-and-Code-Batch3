"""
User-related CRUD operations for authentication and user management.
"""

import sqlite3
from datetime import datetime
import uuid
from typing import Optional, Tuple
from ..database.connection import get_db_connection


def get_user(username: str, password: str) -> Optional[Tuple]:
    """Get user by username and password for authentication."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password)
    )
    user = cur.fetchone()
    conn.close()
    return user


def get_user_by_username(username: str) -> Optional[Tuple]:
    """Get user by username only."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()
    return user


def create_user(username: str, email: str, password: str) -> bool:
    """Create a new user account."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO users (id, username, email, password, created_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, email, password, datetime.now().isoformat()),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user_by_id(user_id: str) -> Optional[Tuple]:
    """Get user by user ID."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user


def update_user_role(user_id: str, role: str) -> bool:
    """Update user role (admin functionality)."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE users SET role = ? WHERE id = ?", (role, user_id)
        )
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


def delete_user(user_id: str) -> bool:
    """Delete user account (admin functionality)."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close() 