"""
Article-related API routes for news article management.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from datetime import datetime, timedelta
import json
from typing import List, Dict, Any
from ..core.schemas import SaveArticle, SearchRequest
from .. import crud
from ..utils.auth import get_current_user

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/today", summary="Get recent articles")
def get_today_articles(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=20, description="Articles per page"),
    current_user: dict = Depends(get_current_user)
):
    """Get recent articles from the last 7 days with pagination."""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    articles_raw = crud.get_articles_by_date_range(start_date, end_date, page, limit)
    total_count = crud.get_articles_count_by_range(start_date, end_date)
    
    articles = _format_articles(articles_raw)
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


@router.get("/date-range/{start_date}/{end_date}", summary="Get articles by date range")
def get_articles_by_range(
    start_date: str, 
    end_date: str, 
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=20, description="Articles per page"),
    current_user: dict = Depends(get_current_user)
):
    """Get articles within a specific date range with pagination."""
    articles_raw = crud.get_articles_by_date_range(start_date, end_date, page, limit)
    total_count = crud.get_articles_count_by_range(start_date, end_date)
    
    articles = _format_articles(articles_raw)
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


@router.get("/today/{category}", summary="Get recent articles by category")
def get_today_articles_by_category(
    category: str, 
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=20, description="Articles per page"),
    current_user: dict = Depends(get_current_user)
):
    """Get recent articles by category from the last 7 days."""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    articles_raw = crud.get_articles_by_date_range_and_category(
        start_date, end_date, category, page, limit
    )
    total_count = crud.get_articles_count_by_range(start_date, end_date, category)
    
    articles = _format_articles(articles_raw)
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


@router.get("/date-range/{start_date}/{end_date}/{category}", summary="Get articles by date range and category")
def get_articles_by_range_and_category(
    start_date: str,
    end_date: str,
    category: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=20, description="Articles per page"),
    current_user: dict = Depends(get_current_user),
):
    """Get articles within date range and category with pagination."""
    articles_raw = crud.get_articles_by_date_range_and_category(
        start_date, end_date, category, page, limit
    )
    total_count = crud.get_articles_count_by_range(start_date, end_date, category)
    
    articles = _format_articles(articles_raw)
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


@router.post("/search", summary="Search articles")
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
    
    articles = _format_articles(articles_raw)
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


@router.get("/{article_id}/stats", summary="Get article reaction stats")
def get_article_stats_endpoint(
    article_id: str, current_user: dict = Depends(get_current_user)
):
    """Get like and dislike statistics for an article."""
    likes, dislikes = crud.get_article_reaction_stats(article_id)
    return {"likes": likes, "dislikes": dislikes}


def _format_articles(articles_raw: List[tuple]) -> List[Dict[str, Any]]:
    """Format raw article tuples into dictionaries."""
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
    return articles 