from services.auth_service import AuthService
from menus.admin_menu import AdminMenu
from menus.user_menu import UserMenu
from utils.validation import (
    validate_signup_data,
    validate_login_data,
    clean_input,
    sanitize_input,
)
from utils.display import DisplayUtils


class AuthHandler:
    """Handler for user authentication operations including login and signup."""

    def __init__(self):
        self.auth_service = AuthService()
        self.display = DisplayUtils()

    def signup(self) -> None:
        """Handle user registration process."""
        print("\nSIGN UP")
        print("=" * 8)

        username = clean_input(input("Username: "))
        email = clean_input(input("Email: "))
        password = input("Password: ")

        is_valid, error_message = validate_signup_data(username, email, password)
        if not is_valid:
            print(self.display.format_error_message(error_message))
            input("Press Enter to continue...")
            return

        username = sanitize_input(username)
        email = sanitize_input(email)

        result = self.auth_service.signup(username, email, password)

        if "error" in result:
            print(
                self.display.format_error_message(f"Signup failed: {result['error']}")
            )
        else:
            print(
                self.display.format_success_message(
                    "Signup successful! You can now login."
                )
            )

        input("Press Enter to continue...")

    def login(self) -> None:
        """Handle user authentication and route to appropriate menu."""
        print("\nLOGIN")
        print("=" * 6)

        username = clean_input(input("Username: "))
        password = input("Password: ")

        is_valid, error_message = validate_login_data(username, password)
        if not is_valid:
            print(self.display.format_error_message(error_message))
            input("Press Enter to continue...")
            return

        username = sanitize_input(username)
        result = self.auth_service.login(username, password)

        if "error" in result:
            print(self.display.format_error_message(f"Login failed: {result['error']}"))
            input("Press Enter to continue...")
            return

        token = result.get("access_token")
        if not token:
            print(self.display.format_error_message("Login failed: No token received."))
            input("Press Enter to continue...")
            return

        payload = self.auth_service.decode_token(token)
        if "error" in payload:
            print(
                self.display.format_error_message(
                    f"Token decode failed: {payload['error']}"
                )
            )
            input("Press Enter to continue...")
            return

        print(self.display.format_success_message("Login successful!"))

        if payload.get("role") == "admin":
            AdminMenu(token).run()
        else:
            UserMenu(token, payload.get("username", username)).run()
