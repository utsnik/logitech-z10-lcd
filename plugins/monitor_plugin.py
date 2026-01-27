from .base import BasePlugin
from PIL import Image, ImageDraw, ImageFont
import psutil
import time
from datetime import datetime

class MonitorPlugin(BasePlugin):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.name = "System Monitor"
        self.cpu = 0
        self.last_stats_check = 0
        
        # Load Fonts
        try:
            self.font_large = ImageFont.truetype("arial.ttf", 16)
            self.font_med = ImageFont.truetype("arialbd.ttf", 11)
            self.font_small = ImageFont.truetype("arial.ttf", 9)
        except IOError:
            self.font_large = ImageFont.load_default()
            self.font_med = ImageFont.load_default()
            self.font_small = ImageFont.load_default()

    def update(self):
        img = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(img)
        
        # Throttle CPU stats to 1Hz
        if time.time() - self.last_stats_check > 1.0:
            self.cpu = int(psutil.cpu_percent())
            self.last_stats_check = time.time()
            
        ram = int(psutil.virtual_memory().percent)
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        date_str = now.strftime("%a %d %b").upper()
        
        # Draw Layout
        draw.text((1, -2), time_str, font=self.font_large, fill=1)
        draw.text((3, 22), date_str, font=self.font_small, fill=1)
        draw.line([55, 2, 55, 40], fill=1)
        
        draw.text((60, 2), f"CPU: {self.cpu}%", font=self.font_med, fill=1)
        draw.text((60, 14), f"RAM: {ram}%", font=self.font_med, fill=1)
        
        # Graph
        draw.rectangle([60, 28, 156, 38], outline=1)
        fill = int((self.cpu / 100.0) * 94)
        if fill > 0:
            # Clamp fill to maximum width
            fill = min(fill, 94)
            draw.rectangle([62, 30, 62 + fill, 36], fill=1)
            
        return img
