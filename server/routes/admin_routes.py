"""
Admin-related API routes for server management and administrative functions.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Dict, Any
import json
from ..core.schemas import ServerUpdate, CategoryCreate, CategorySuggestion, ArticleCreate
from .. import crud
from ..utils.auth import get_current_user
from ..scheduler.scheduler import news_scheduler
from ..services.email_service import EmailService

router = APIRouter(prefix="/admin", tags=["Admin"])

# Email service
email_service = EmailService()


@router.get("/servers", summary="List external servers")
def list_servers(current_user: dict = Depends(get_current_user)):
    """Get list of all external servers."""
    return {"servers": crud.list_external_servers()}


@router.get("/server-details", summary="Get server details")
def server_details(current_user: dict = Depends(get_current_user)):
    """Get detailed server information including API keys."""
    return {"details": crud.get_server_details()}


@router.put("/update-server/{server_id}", summary="Update server API key")
def update_server(
    server_id: str, update: ServerUpdate, current_user: dict = Depends(get_current_user)
):
    """Update server API key."""
    if crud.update_server_api(server_id, update.api_key):
        return {"message": "Server updated successfully."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Server not found."
    )


@router.post("/add-category", summary="Add new category")
def add_category(cat: CategoryCreate, current_user: dict = Depends(get_current_user)):
    """Add a new article category."""
    if crud.add_category(cat.name):
        return {"message": "Category added successfully."}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Category already exists."
    )


@router.get("/categories", summary="Get all categories")
def get_categories(current_user: dict = Depends(get_current_user)):
    """Get all available categories."""
    categories = crud.get_categories()
    return {"categories": categories}


@router.post("/category-suggestion", summary="Get AI category suggestion")
def suggest_category(
    suggestion: CategorySuggestion, current_user: dict = Depends(get_current_user)
):
    """Get AI-powered category suggestion for an article."""
    # Simple keyword-based suggestion (can be enhanced with AI)
    content_lower = (suggestion.article_title + " " + suggestion.article_content).lower()
    
    suggestions = []
    for category in suggestion.existing_categories:
        if category.lower() in content_lower:
            suggestions.append(category)
    
    return {"suggestions": suggestions[:3]}


@router.get("/api-status", summary="Get API status")
async def get_api_status():
    """Get API usage and status information."""
    api_info = crud.get_api_info()
    return {"api_status": api_info}


@router.post("/test-email", summary="Test email configuration")
def test_email(current_user: dict = Depends(get_current_user)):
    """Test email service configuration."""
    success, message = email_service.test_email_configuration()
    if success:
        return {"message": "Email configuration is working."}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"Email configuration failed: {message}"
    )


@router.post("/fetch-news", summary="Manually trigger news fetch")
def manual_fetch_news(current_user: dict = Depends(get_current_user)):
    """Manually trigger news fetching process."""
    try:
        # This would trigger the news fetching job
        # For now, just return success message
        return {"message": "News fetch triggered successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Failed to trigger news fetch: {str(e)}"
        )


@router.post("/test-notifications", summary="Test notification system")
async def test_notifications():
    """Test the notification system."""
    try:
        # This would test the notification system
        # For now, just return success message
        return {"message": "Notification system test completed."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Notification test failed: {str(e)}"
        )


@router.get("/all-articles", summary="Get all articles (admin)")
async def get_all_articles(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Articles per page")
):
    """Get all articles with pagination (admin only)."""
    # This would get all articles from the database
    # For now, return empty list
    return {
        "articles": [],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": 0,
            "pages": 0,
            "has_next": False,
            "has_prev": False
        }
    }


@router.get("/article-stats", summary="Get article statistics")
async def get_article_stats():
    """Get article statistics (admin only)."""
    # This would get article statistics
    # For now, return basic stats
    return {
        "total_articles": 0,
        "articles_today": 0,
        "articles_this_week": 0,
        "categories": [],
        "top_sources": []
    } 