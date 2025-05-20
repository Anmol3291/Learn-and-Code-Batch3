from abc import ABC, abstractmethod


class Button(ABC):
    """Abstract base class for button UI component."""

    @abstractmethod
    def render(self):
        """Render the button on screen."""
        pass

    @abstractmethod
    def on_click(self):
        """Handle button click event."""
        pass


class Checkbox(ABC):
    """Abstract base class for checkbox UI component."""

    @abstractmethod
    def render(self):
        """Render the checkbox on screen."""
        pass

    @abstractmethod
    def toggle(self):
        """Toggle the checkbox state."""
        pass


class TextField(ABC):
    """Abstract base class for text field UI component."""

    @abstractmethod
    def render(self):
        """Render the text field on screen."""
        pass

    @abstractmethod
    def on_input(self, value):
        """Handle text input event."""
        pass
