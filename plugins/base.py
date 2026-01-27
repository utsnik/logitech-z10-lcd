from abc import ABC, abstractmethod
from PIL import Image

class BasePlugin(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.name = "Unknown Plugin"

    @abstractmethod
    def update(self):
        """
        Called every frame.
        Should return a PIL Image object to display, or None if no update.
        """
        pass

    def handle_input(self, data):
        """
        Called when button input is received.
        data: List of integers (raw bytes)
        Returns: True if input was handled, False otherwise.
        """
        return False

    def on_enter(self):
        """Called when this plugin becomes active."""
        pass

    def on_exit(self):
        """Called when this plugin becomes inactive."""
        pass
