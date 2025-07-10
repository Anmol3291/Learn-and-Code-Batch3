"""
Reaction-related API routes for article likes and dislikes.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
import json
from typing import List, Dict, Any
from ..core.schemas import SaveArticle
from .. import crud
from ..utils.auth import get_current_user

router = APIRouter(prefix="/articles", tags=["Reactions"])


@router.post("/like", summary="Like an article")
def like_article_endpoint(
    reaction_data: SaveArticle, current_user: dict = Depends(get_current_user)
):
    """Like an article and update article stats."""
    if crud.like_article(reaction_data.username, reaction_data.article_id):
        return {"message": "Article liked successfully."}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Article already liked or not found."
    )


@router.post("/dislike", summary="Dislike an article")
def dislike_article_endpoint(
    reaction_data: SaveArticle, current_user: dict = Depends(get_current_user)
):
    """Dislike an article and update article stats."""
    if crud.dislike_article(reaction_data.username, reaction_data.article_id):
        return {"message": "Article disliked successfully."}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Article already disliked or not found."
    )


@router.delete("/like", summary="Remove like from article")
def unlike_article_endpoint(
    reaction_data: SaveArticle, current_user: dict = Depends(get_current_user)
):
    """Remove like from article and update stats."""
    if crud.unlike_article(reaction_data.username, reaction_data.article_id):
        return {"message": "Like removed successfully."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Like not found."
    )


@router.delete("/dislike", summary="Remove dislike from article")
def remove_dislike_endpoint(
    reaction_data: SaveArticle, current_user: dict = Depends(get_current_user)
):
    """Remove dislike from article and update stats."""
    if crud.remove_dislike(reaction_data.username, reaction_data.article_id):
        return {"message": "Dislike removed successfully."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Dislike not found."
    )


@router.get("/liked/{username}", summary="Get user's liked articles")
def get_liked_articles_endpoint(
    username: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=20, description="Articles per page"),
    current_user: dict = Depends(get_current_user)
):
    """Get articles liked by user with pagination."""
    articles_raw = crud.get_liked_articles(username, page, limit)
    total_count = crud.get_liked_articles_count(username)
    
    articles = _format_reaction_articles(articles_raw)
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


@router.get("/disliked/{username}", summary="Get user's disliked articles")
def get_disliked_articles_endpoint(
    username: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=20, description="Articles per page"),
    current_user: dict = Depends(get_current_user)
):
    """Get articles disliked by user with pagination."""
    articles_raw = crud.get_disliked_articles(username, page, limit)
    total_count = crud.get_disliked_articles_count(username)
    
    articles = _format_reaction_articles(articles_raw)
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


def _format_reaction_articles(articles_raw: List[tuple]) -> List[Dict[str, Any]]:
    """Format raw reaction article tuples into dictionaries."""
    articles = []
    for article in articles_raw:
        # Handle the reaction_date field that's appended to the article tuple
        if len(article) == 13:  # Article with reaction_date
            article_id, title, content, source, url, category, keywords, published_date, created_at, likes, dislikes, vector_id, reaction_date = article
        else:  # Regular article
            article_id, title, content, source, url, category, keywords, published_date, created_at, likes, dislikes, vector_id = article
            reaction_date = None
            
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
            'reaction_date': reaction_date
        })
    return articles 