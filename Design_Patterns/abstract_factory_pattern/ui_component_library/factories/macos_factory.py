from ui_component_library.interfaces.ui_factory import UIFactory
from ui_component_library.macos.macos_components import (
    MacOSButton,
    MacOSCheckbox,
    MacOSTextField,
)


class MacOSUIFactory(UIFactory):
    """Factory for creating MacOS UI components."""

    def create_button(self):
        """Create a MacOS-style button."""
        return MacOSButton()

    def create_checkbox(self):
        """Create a MacOS-style checkbox."""
        return MacOSCheckbox()

    def create_text_field(self):
        """Create a MacOS-style text field."""
        return MacOSTextField()
