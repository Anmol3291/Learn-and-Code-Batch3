from ui_component_library.interfaces.ui_factory import UIFactory
from ui_component_library.windows.windows_components import (
    WindowsButton,
    WindowsCheckbox,
    WindowsTextField,
)


class WindowsUIFactory(UIFactory):
    """Factory for creating Windows UI components."""

    def create_button(self):
        """Create a Windows-style button."""
        return WindowsButton()

    def create_checkbox(self):
        """Create a Windows-style checkbox."""
        return WindowsCheckbox()

    def create_text_field(self):
        """Create a Windows-style text field."""
        return WindowsTextField()
