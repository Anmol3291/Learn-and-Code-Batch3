"""
API routes module - imports all route modules.
"""

from .auth_routes import router as auth_router
from .article_routes import router as article_router
from .saved_article_routes import router as saved_article_router, client_router as saved_article_client_router
from .reaction_routes import router as reaction_router
from .notification_routes import router as notification_router
from .admin_routes import router as admin_router 