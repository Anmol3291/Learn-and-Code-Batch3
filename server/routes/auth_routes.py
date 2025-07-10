"""
Authentication-related API routes for user registration and login.
"""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
from jose import jwt
from ..core.schemas import UserCreate, UserLogin
from .. import crud
from ..services.email_service import EmailService
from ..utils.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Email service
email_service = EmailService()


@router.post("/signup", summary="Register new user")
def signup(user: UserCreate):
    """Register a new user account."""
    if crud.create_user(user.username, user.email, user.password):
        # Send welcome email
        email_service.send_welcome_email(user.email, user.username)
        return {"message": "User created successfully."}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Username or email already exists."
    )


@router.post("/login", summary="User login")
def login(user: UserLogin):
    """Authenticate user and return access token."""
    found_user = crud.get_user(user.username, user.password)
    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials."
        )

    access_token = create_access_token(
        data={"username": found_user[1], "role": found_user[4]}
    )
    return {"access_token": access_token, "token_type": "bearer"} 