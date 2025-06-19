import re


class InputValidator:
    """Utility class for input validation"""

    @staticmethod
    def validate_integer(value: str) -> bool:
        """Validate if string can be converted to integer"""
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        """
        Comprehensive email validation with detailed error messages
        Returns: (is_valid, error_message)
        """
        if not email or not email.strip():
            return False, "Email cannot be empty"

        email = email.strip()

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_pattern, email):
            return False, "Invalid email format. Please use format: example@domain.com"

        if ".." in email:
            return False, "Email cannot contain consecutive dots"

        local_part = email.split("@")[0]
        if local_part.startswith(".") or local_part.endswith("."):
            return False, "Email cannot start or end with a dot before @"

        if len(email) > 254:
            return False, "Email is too long (maximum 254 characters)"

        if len(local_part) > 64:
            return (
                False,
                "Email local part is too long (maximum 64 characters before @)",
            )

        return True, ""

    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """
        Comprehensive password validation with detailed error messages
        Password requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)
        Returns: (is_valid, error_message)
        """
        if not password:
            return False, "Password cannot be empty"

        errors = []

        if len(password) < 8:
            errors.append("at least 8 characters")

        if not re.search(r"[A-Z]", password):
            errors.append("at least one uppercase letter")

        if not re.search(r"[a-z]", password):
            errors.append("at least one lowercase letter")

        if not re.search(r"\d", password):
            errors.append("at least one digit")

        if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", password):
            errors.append("at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)")

        if len(password) > 128:
            errors.append("maximum 128 characters")

        if password.lower() in ["password", "12345678", "hello@123", "admin123"]:
            errors.append("cannot be a common weak password")

        if re.search(r"(.)\1{3,}", password):
            errors.append("cannot have more than 3 consecutive identical characters")

        if errors:
            error_message = f"Password must contain {', '.join(errors)}"
            return False, error_message

        return True, ""

    @staticmethod
    def validate_username(username: str) -> tuple[bool, str]:
        """
        Username validation with detailed error messages
        Username requirements:
        - 3-30 characters
        - Only letters, numbers, underscores, and hyphens
        - Cannot start or end with underscore or hyphen
        Returns: (is_valid, error_message)
        """
        if not username or not username.strip():
            return False, "Username cannot be empty"

        username = username.strip()

        if len(username) < 3:
            return False, "Username must be at least 3 characters long"

        if len(username) > 30:
            return False, "Username cannot be longer than 30 characters"

        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            return (
                False,
                "Username can only contain letters, numbers, underscores, and hyphens",
            )

        if username.startswith(("_", "-")) or username.endswith(("_", "-")):
            return False, "Username cannot start or end with underscore or hyphen"

        if re.search(r"[_-]{2,}", username):
            return False, "Username cannot have consecutive underscores or hyphens"

        return True, ""

    @staticmethod
    def validate_non_empty(value: str) -> bool:
        """Validate non-empty string"""
        return bool(value and value.strip())

    @staticmethod
    def validate_choice(choice: str, valid_choices: list) -> bool:
        """Validate choice against valid options"""
        return choice in valid_choices
