"""
News Aggregator API - Main FastAPI application.
"""

from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
from typing import List, Dict, Any

# Import route modules
from .routes import (
    auth_router, article_router, saved_article_router, saved_article_client_router,
    reaction_router, notification_router, admin_router
)
from .core.schemas import SearchRequest, KeywordConfig
from . import crud
from .utils.auth import get_current_user

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="News Aggregator API",
    version="1.0.0",
    description="A comprehensive news aggregation and notification system",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(auth_router)
app.include_router(article_router)
app.include_router(saved_article_router)
app.include_router(saved_article_client_router)
app.include_router(reaction_router)
app.include_router(notification_router)
app.include_router(admin_router)


@app.post("/search", summary="Search articles")
def search_articles(
    search_request: SearchRequest,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=20, description="Articles per page"),
    current_user: dict = Depends(get_current_user)
):
    """Search articles with filters and pagination."""
    articles_raw = crud.search_articles(
        search_request.query,
        search_request.category,
        search_request.date_from,
        search_request.date_to,
        page,
        limit
    )
    total_count = crud.search_articles_count(
        search_request.query,
        search_request.category,
        search_request.date_from,
        search_request.date_to
    )
    
    articles = []
    for article in articles_raw:
        article_id, title, content, source, url, category, keywords, published_date, created_at, likes, dislikes, vector_id = article
        articles.append({
            'id': article_id,
            'title': title,
            'content': content,
            'source': source,
            'url': url,
            'category': category,
            'keywords': json.loads(keywords) if keywords else [],
            'published_date': published_date,
            'created_at': created_at,
            'likes': likes,
            'dislikes': dislikes
        })
    
    total_pages = (total_count + limit - 1) // limit
    
    return {
        "articles": articles,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total_count,
            "pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }


@app.post("/keywords", summary="Update user keywords")
def update_keywords(
    keyword_config: KeywordConfig, current_user: dict = Depends(get_current_user)
):
    """Update user's keyword preferences."""
    if crud.update_user_keywords(username=keyword_config.username, keywords=keyword_config.keywords):
        return {"message": "Keywords updated successfully."}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Failed to update keywords."
    )


@app.get("/categories", summary="Get all categories")
def get_categories():
    """Get all available categories."""
    categories = crud.get_categories()
    return {"categories": categories}


# Global scheduler instance
news_scheduler = None

@app.on_event("startup")
async def startup_event():
    """Start the news scheduler on application startup."""
    global news_scheduler
    try:
        from .scheduler.scheduler import NewsScheduler
        news_scheduler = NewsScheduler()
        news_scheduler.start()
        logger.info("News scheduler started successfully")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop the news scheduler on application shutdown."""
    global news_scheduler
    try:
        if news_scheduler:
            news_scheduler.stop()
            logger.info("News scheduler stopped successfully")
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")


@app.get("/", summary="API Root")
def root():
    """API root endpoint."""
    return {
        "message": "News Aggregator API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", summary="Health Check")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "news-aggregator-api"} 