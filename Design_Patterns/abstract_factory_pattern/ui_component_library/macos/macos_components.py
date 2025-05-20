from ui_component_library.interfaces.ui_components import Button, Checkbox, TextField


class MacOSButton(Button):
    """MacOS-specific implementation of button."""

    def render(self):
        """Render a MacOS-style button."""
        return "Rendering a MacOS-style button"

    def on_click(self):
        """Handle MacOS button click event."""
        return "MacOS button clicked"


class MacOSCheckbox(Checkbox):
    """MacOS-specific implementation of checkbox."""

    def render(self):
        """Render a MacOS-style checkbox."""
        return "Rendering a MacOS-style checkbox"

    def toggle(self):
        """Toggle the MacOS checkbox state."""
        return "MacOS checkbox toggled"


class MacOSTextField(TextField):
    """MacOS-specific implementation of text field."""

    def render(self):
        """Render a MacOS-style text field."""
        return "Rendering a MacOS-style text field"

    def on_input(self, value):
        """Handle MacOS text field input event."""
        return f"MacOS text field input: {value}"
