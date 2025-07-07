"""
Server-related CRUD operations for external API server management.
"""

import sqlite3
from datetime import datetime
from typing import List, Tuple
from ..database.connection import get_db_connection


def list_external_servers() -> List[Tuple]:
    """Get list of all external servers with basic info."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, status, last_access, priority FROM external_servers ORDER BY priority")
    servers = cur.fetchall()
    conn.close()
    return servers


def get_server_details() -> List[Tuple]:
    """Get detailed server information including API keys."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, api_key, priority FROM external_servers ORDER BY priority")
    details = cur.fetchall()
    conn.close()
    return details


def update_server_api(server_id: str, api_key: str) -> bool:
    """Update server API key and return success status."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if server exists
    cur.execute("SELECT id FROM external_servers WHERE id = ?", (server_id,))
    if not cur.fetchone():
        conn.close()
        return False
    
    # Update the server
    cur.execute(
        "UPDATE external_servers SET api_key = ?, last_access = ? WHERE id = ?", 
        (api_key, datetime.now().isoformat(), server_id)
    )
    updated_rows = cur.rowcount
    conn.commit()
    conn.close()
    
    return updated_rows > 0


def update_server_status(server_id: str, status: str, last_access: str) -> bool:
    """Update server status and last access time."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE external_servers SET status = ?, last_access = ? WHERE id = ?",
            (status, last_access, server_id)
        )
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


def get_api_info() -> List[Tuple]:
    """Get API usage information for all servers."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            id, name, status, last_access, priority,
            (SELECT COUNT(*) FROM articles WHERE source = external_servers.name) as articles_count
        FROM external_servers 
        ORDER BY priority
    """)
    info = cur.fetchall()
    conn.close()
    return info


def reset_api_daily_counters() -> bool:
    """Reset daily API usage counters (called by scheduler)."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # This would be used if we implement API rate limiting
        # For now, just update last access times
        cur.execute("UPDATE external_servers SET last_access = ?", (datetime.now().isoformat(),))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close() 