"""
Pydantic schemas for request/response validation and data transfer objects.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List


# Authentication Schemas
class UserCreate(BaseModel):
    """Schema for user registration requests."""
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema for user authentication requests."""
    username: str
    password: str


# Server Management Schemas
class ServerUpdate(BaseModel):
    """Schema for updating server API keys."""
    api_key: str


# Category Management Schemas
class CategoryCreate(BaseModel):
    """Schema for creating new article categories."""
    name: str


class CategorySuggestion(BaseModel):
    """Schema for AI-powered category suggestions."""
    article_title: str
    article_content: str
    existing_categories: List[str]


# Article Management Schemas
class ArticleCreate(BaseModel):
    """Schema for creating new articles."""
    title: str
    content: str
    source: str
    url: str
    category: Optional[str] = None
    keywords: Optional[List[str]] = None
    published_date: str
    image_url: Optional[str] = None


class SaveArticle(BaseModel):
    """Schema for saving articles to user collections."""
    username: str
    article_id: str


class DeleteSavedArticle(BaseModel):
    """Schema for removing articles from user collections."""
    username: str
    article_id: str


# Search Schemas
class SearchRequest(BaseModel):
    """Schema for article search requests with filters."""
    query: str
    category: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None


# Notification Schemas
class NotificationConfig(BaseModel):
    """Schema for configuring user notification preferences."""
    username: str
    category: str
    enabled: bool


class KeywordConfig(BaseModel):
    """Schema for configuring user keyword preferences."""
    username: str
    keywords: List[str] 