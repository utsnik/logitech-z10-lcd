from .base import BasePlugin
from PIL import Image, ImageDraw, ImageFont
import time

class DebugPlugin(BasePlugin):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.name = "Button Mapper"
        self.last_input = []
        self.font = ImageFont.load_default()
        try:
             self.font = ImageFont.truetype("arial.ttf", 10)
        except:
             pass

    def update(self):
        img = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(img)
        
        draw.text((5, 0), "PLUGIN SYSTEM: DEBUG", font=self.font, fill=1)
        draw.line([0, 12, 160, 12], fill=1)
        
        if self.last_input:
            # Show the raw bytes
            hex_str = ' '.join(f'{x:02X}' for x in self.last_input[:8]) # Show first 8 bytes
            draw.text((5, 15), f"Last Input:", font=self.font, fill=1)
            draw.text((5, 28), hex_str, font=self.font, fill=1)
        else:
            draw.text((5, 20), "Press any button...", font=self.font, fill=1)
            
        return img

    def handle_input(self, data):
        self.last_input = data
        return True
