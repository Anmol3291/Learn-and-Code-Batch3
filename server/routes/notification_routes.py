"""
Notification-related API routes for user notifications and preferences.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Any
from ..core.schemas import NotificationConfig, KeywordConfig
from .. import crud
from ..utils.auth import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/{username}", summary="Get user notifications")
def get_notifications(username: str, current_user: dict = Depends(get_current_user)):
    """Get all notifications for a user."""
    notifications_raw = crud.get_user_notifications(username)
    
    notifications = []
    for notification in notifications_raw:
        notification_id, user_id, article_id, notification_type, message, sent_at, email_sent, title, url = notification
        notifications.append({
            'id': notification_id,
            'article_id': article_id,
            'notification_type': notification_type,
            'message': message,
            'sent_at': sent_at,
            'email_sent': bool(email_sent),
            'article_title': title,
            'article_url': url
        })
    
    return {"notifications": notifications}


@router.delete("/{username}/{notification_id}", summary="Delete specific notification")
def delete_notification_endpoint(
    username: str, notification_id: str, current_user: dict = Depends(get_current_user)
):
    """Delete a specific notification."""
    if crud.delete_notification(notification_id):
        return {"message": "Notification deleted successfully."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Notification not found."
    )


@router.delete("/{username}", summary="Delete all user notifications")
def delete_all_notifications_endpoint(
    username: str, current_user: dict = Depends(get_current_user)
):
    """Delete all notifications for a user."""
    if crud.delete_user_notifications(username):
        return {"message": "All notifications deleted successfully."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="User not found."
    )


@router.get("/config/{username}", summary="Get notification preferences")
def get_notification_config(username: str, current_user: dict = Depends(get_current_user)):
    """Get user's notification preferences by category."""
    config = crud.get_user_notification_config(username)
    return {"config": config}


@router.post("/config", summary="Update notification preferences")
def update_notification_config(
    config: NotificationConfig, current_user: dict = Depends(get_current_user)
):
    """Update user's notification preference for a category."""
    if crud.update_user_notification_config(username=config.username, category=config.category, enabled=config.enabled):
        return {"message": "Notification preference updated successfully."}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Failed to update notification preference."
    )


@router.get("/keywords/{username}", summary="Get user keywords")
def get_keywords(username: str, current_user: dict = Depends(get_current_user)):
    """Get user's keyword preferences."""
    keywords = crud.get_user_keywords(username)
    return {"keywords": keywords}


@router.post("/keywords", summary="Update user keywords")
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