from abc import ABC, abstractmethod


class UIFactory(ABC):
    """Abstract factory interface for creating UI component families."""

    @abstractmethod
    def create_button(self):
        """Create a button component."""
        pass

    @abstractmethod
    def create_checkbox(self):
        """Create a checkbox component."""
        pass

    @abstractmethod
    def create_text_field(self):
        """Create a text field component."""
        pass
