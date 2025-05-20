from ui_component_library.interfaces.ui_components import Button, Checkbox, TextField


class WindowsButton(Button):
    """Windows-specific implementation of button."""

    def render(self):
        """Render a Windows-style button."""
        return "Rendering a Windows-style button"

    def on_click(self):
        """Handle Windows button click event."""
        return "Windows button clicked"


class WindowsCheckbox(Checkbox):
    """Windows-specific implementation of checkbox."""

    def render(self):
        """Render a Windows-style checkbox."""
        return "Rendering a Windows-style checkbox"

    def toggle(self):
        """Toggle the Windows checkbox state."""
        return "Windows checkbox toggled"


class WindowsTextField(TextField):
    """Windows-specific implementation of text field."""

    def render(self):
        """Render a Windows-style text field."""
        return "Rendering a Windows-style text field"

    def on_input(self, value):
        """Handle Windows text field input event."""
        return f"Windows text field input: {value}"
