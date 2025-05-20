from ui_component_library.factories.windows_factory import WindowsUIFactory
from ui_component_library.factories.macos_factory import MacOSUIFactory
from ui_component_library.client.ui_application import UIApplication


def main():
    try:
        os_type = input("Enter OS type (windows, macos): ").lower()

        if os_type == "windows":
            factory = WindowsUIFactory()
        elif os_type == "macos":
            factory = MacOSUIFactory()
        else:
            raise ValueError(f"Unsupported OS type: {os_type}")

        app = UIApplication(factory)
        app.create_ui()

        ui_elements = app.render_ui()
        for element in ui_elements:
            print(element)

        print(app.button.on_click())
        print(app.checkbox.toggle())
        print(app.text_field.on_input("Hello, World!"))

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
