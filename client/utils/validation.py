import re
from typing import Tuple


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


# Validation constants
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20
EMAIL_MAX_LENGTH = 100
PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 50

# Regex patterns
USERNAME_PATTERN = r'^[a-zA-Z0-9_-]+$'
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
DANGEROUS_CHARS = ['<', '>', '"', "'", '&', ';', '|', '`', '$', '(', ')', '{', '}']


def validate_username(username: str) -> Tuple[bool, str]:
    """Validate username format and requirements."""
    if not username:
        return False, "Username cannot be empty"
    
    if len(username) < USERNAME_MIN_LENGTH:
        return False, f"Username must be at least {USERNAME_MIN_LENGTH} characters long"
    
    if len(username) > USERNAME_MAX_LENGTH:
        return False, f"Username must be less than {USERNAME_MAX_LENGTH} characters"
    
    if not re.match(USERNAME_PATTERN, username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    
    if not re.match(r'^[a-zA-Z0-9]', username):
        return False, "Username must start with a letter or number"
    
    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format and requirements."""
    if not email:
        return False, "Email cannot be empty"
    
    if not re.match(EMAIL_PATTERN, email):
        return False, "Please enter a valid email address"
    
    if len(email) > EMAIL_MAX_LENGTH:
        return False, f"Email address must be less than {EMAIL_MAX_LENGTH} characters"
    
    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength and requirements."""
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"
    
    if len(password) > PASSWORD_MAX_LENGTH:
        return False, f"Password must be less than {PASSWORD_MAX_LENGTH} characters"
    
    if not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, ""


def validate_signup_data(username: str, email: str, password: str) -> Tuple[bool, str]:
    """Validate all signup form data comprehensively."""
    username_valid, username_error = validate_username(username)
    if not username_valid:
        return False, username_error
    
    email_valid, email_error = validate_email(email)
    if not email_valid:
        return False, email_error
    
    password_valid, password_error = validate_password(password)
    if not password_valid:
        return False, password_error
    
    return True, ""


def validate_login_data(username: str, password: str) -> Tuple[bool, str]:
    """Validate login form data."""
    if not username:
        return False, "Username cannot be empty"
    
    if not password:
        return False, "Password cannot be empty"
    
    return True, ""


def clean_input(text: str) -> str:
    """Remove extra whitespace from user input."""
    return text.strip() if text else ""


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not text:
        return ""
    
    for char in DANGEROUS_CHARS:
        text = text.replace(char, '')
    
    return text.strip() 