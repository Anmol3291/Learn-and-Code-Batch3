"""
Database connection and initialization module.
"""

import sqlite3
from datetime import datetime
import uuid
import os
import logging

# Database configuration
DB_NAME = "news_app.db"

# Configure logger
logger = logging.getLogger(__name__)


def get_db_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Initialize the database with schema and default data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if database is already initialized
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    tables_exist = cursor.fetchone()
    
    if not tables_exist:
        logger.info("Database not found, creating new schema...")
        _create_tables(cursor)
        _insert_default_data(cursor)
        conn.commit()
        logger.info("Database initialized successfully with new schema")
    else:
        logger.info("Database already exists, skipping initialization")
    
    conn.close()


def _create_tables(cursor):
    """Create all database tables with proper schema."""
    _create_users_table(cursor)
    _create_external_servers_table(cursor)
    _create_categories_table(cursor)
    _create_articles_table(cursor)
    _create_saved_articles_table(cursor)
    _create_user_notifications_table(cursor)
    _create_user_keywords_table(cursor)
    _create_notifications_table(cursor)
    _create_vector_store_table(cursor)
    _create_article_reactions_table(cursor)


def _create_users_table(cursor):
    """Create users table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        )
    """)


def _create_external_servers_table(cursor):
    """Create external servers table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS external_servers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            api_key TEXT NOT NULL,
            last_access TEXT NOT NULL,
            priority INTEGER DEFAULT 1
        )
    """)


def _create_categories_table(cursor):
    """Create categories table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
    """)


def _create_articles_table(cursor):
    """Create articles table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT,
            url TEXT,
            category TEXT,
            keywords TEXT,
            published_date TEXT,
            created_at TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            dislikes INTEGER DEFAULT 0,
            vector_id TEXT
        )
    """)


def _create_saved_articles_table(cursor):
    """Create saved articles table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_articles (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            article_id TEXT,
            saved_at TEXT NOT NULL,
            FOREIGN KEY(article_id) REFERENCES articles(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)


def _create_article_reactions_table(cursor):
    """Create article reactions table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS article_reactions (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            article_id TEXT NOT NULL,
            reaction_type TEXT NOT NULL CHECK (reaction_type IN ('like', 'dislike')),
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (article_id) REFERENCES articles (id),
            UNIQUE(user_id, article_id, reaction_type)
        )
    """)


def _create_user_notifications_table(cursor):
    """Create user notifications table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_notifications (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            category TEXT,
            enabled BOOLEAN DEFAULT 1,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)


def _create_user_keywords_table(cursor):
    """Create user keywords table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_keywords (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            keywords TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)


def _create_notifications_table(cursor):
    """Create notifications table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            article_id TEXT,
            notification_type TEXT,
            message TEXT,
            sent_at TEXT NOT NULL,
            email_sent BOOLEAN DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(article_id) REFERENCES articles(id)
        )
    """)


def _create_vector_store_table(cursor):
    """Create vector store table."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vector_store (
            id TEXT PRIMARY KEY,
            article_id TEXT,
            vector_data TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(article_id) REFERENCES articles(id)
        )
    """)


def _insert_default_data(cursor):
    """Insert default data into database."""
    _insert_default_admin(cursor)
    _insert_default_servers(cursor)
    _insert_default_categories(cursor)


def _insert_default_admin(cursor):
    """Insert default admin user."""
    admin_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT OR IGNORE INTO users (id, username, email, password, role, created_at)
        VALUES (?, 'admin', 'admin@example.com', 'admin123', 'admin', ?)
    """, (admin_id, datetime.now().isoformat()))


def _insert_default_servers(cursor):
    """Insert default external servers."""
    server1_id = str(uuid.uuid4())
    server2_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT OR IGNORE INTO external_servers (id, name, status, api_key, last_access, priority)
        VALUES
        (?, 'NewsAPI', 'Active', 'f32547e176f6453884dfe2c8d602b306', ?, 1),
        (?, 'TheNewsAPI', 'Active', 'VzE4s2dPcH1vn2YhWbhUm7wGXGIM0fpYJB0R3zfH', ?, 2)
    """, (server1_id, datetime.now().isoformat(), server2_id, datetime.now().isoformat()))


def _insert_default_categories(cursor):
    """Insert default categories."""
    categories = ["Business", "Entertainment", "Sports", "Technology"]
    for category in categories:
        cat_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT OR IGNORE INTO categories (id, name, created_at) VALUES (?, ?, ?)", 
            (cat_id, category, datetime.now().isoformat())
        )


# Initialize database on import
init_db() 