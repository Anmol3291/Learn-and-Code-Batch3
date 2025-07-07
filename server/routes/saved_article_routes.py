"""
Saved article-related API routes for user article collections.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
import json
from typing import List, Dict, Any
from ..core.schemas import SaveArticle, DeleteSavedArticle
from .. import crud
from ..utils.auth import get_current_user

router = APIRouter(prefix="/saved-articles", tags=["Saved Articles"])

# Separate router for client endpoints
client_router = APIRouter(tags=["Client Endpoints"])


@router.post("/save", summary="Save article to user collection")
def save_article_endpoint(
    save_data: SaveArticle, current_user: dict = Depends(get_current_user)
):
    """Save an article to user's collection."""
    if crud.save_article(save_data.username, save_data.article_id):
        return {"message": "Article saved successfully."}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Article already saved or not found."
    )


@client_router.post("/save-article", summary="Save article to user collection (client endpoint)")
def save_article_client_endpoint(
    save_data: SaveArticle, current_user: dict = Depends(get_current_user)
):
    """Save an article to user's collection (client endpoint)."""
    if crud.save_article(save_data.username, save_data.article_id):
        return {"message": "Article saved successfully."}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Article already saved or not found."
    )


@router.get("/{username}", summary="Get user's saved articles")
def get_saved_articles(
    username: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=20, description="Articles per page"),
    current_user: dict = Depends(get_current_user)
):
    """Get user's saved articles with pagination."""
    articles_raw = crud.get_saved_articles(username, page, limit)
    total_count = crud.get_saved_articles_count(username)
    
    articles = _format_saved_articles(articles_raw)
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


@router.delete("/{username}/{article_id}", summary="Remove article from saved collection")
def delete_saved_article_endpoint(
    username: str, article_id: str, current_user: dict = Depends(get_current_user)
):
    """Remove article from user's saved collection."""
    if crud.delete_saved_article(username, article_id):
        return {"message": "Article removed from saved collection."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Article not found in saved collection."
    )


def _format_saved_articles(articles_raw: List[tuple]) -> List[Dict[str, Any]]:
    """Format raw saved article tuples into dictionaries."""
    articles = []
    for article in articles_raw:
        # Handle the saved_at field that's appended to the article tuple
        if len(article) == 13:  # Article with saved_at
            article_id, title, content, source, url, category, keywords, published_date, created_at, likes, dislikes, vector_id, saved_at = article
        else:  # Regular article
            article_id, title, content, source, url, category, keywords, published_date, created_at, likes, dislikes, vector_id = article
            saved_at = None
            
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
            'dislikes': dislikes,
            'saved_at': saved_at
        })
    return articles 