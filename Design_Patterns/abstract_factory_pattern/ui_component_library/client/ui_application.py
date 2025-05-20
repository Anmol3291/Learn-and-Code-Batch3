from ui_component_library.interfaces.ui_factory import UIFactory


class UIApplication:
    """Client application that works with UI components."""

    def __init__(self, factory: UIFactory):
        self.factory = factory
        self.button = None
        self.checkbox = None
        self.text_field = None

    def create_ui(self):
        """Creating all UI components using the factory."""
        self.button = self.factory.create_button()
        self.checkbox = self.factory.create_checkbox()
        self.text_field = self.factory.create_text_field()

    def render_ui(self):
        """Rendering all UI components."""
        button_output = self.button.render()
        checkbox_output = self.checkbox.render()
        text_field_output = self.text_field.render()

        return [button_output, checkbox_output, text_field_output]
