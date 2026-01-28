from .base import BasePlugin
from PIL import Image, ImageDraw, ImageFont
import time
import datetime

class ClockPlugin(BasePlugin):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.name = "Clock"
        try:
            self.font_big = ImageFont.truetype("arialbd.ttf", 34) # Maximize height
            self.font_date = ImageFont.truetype("arial.ttf", 10)
        except:
            self.font_big = ImageFont.load_default()
            self.font_date = ImageFont.load_default()
            
        self.stopwatch_start = 0
        self.stopwatch_paused_at = 0
        self.is_running = False

    def update(self):
        img = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(img)
        
        now = datetime.datetime.now()
        
        # Mode: Standard Clock
        # Time
        time_str = now.strftime("%H:%M")
        # Center the big time
        bbox = draw.textbbox((0,0), time_str, font=self.font_big)
        w = bbox[2] - bbox[0]
        x = (self.width - w) // 2
        draw.text((x, -4), time_str, font=self.font_big, fill=1)
        
        # Second ticker (bar or small text? let's do small text)
        sec_str = now.strftime(":%S")
        draw.text((x + w, 15), sec_str, font=self.font_date, fill=1)
        
        # Date (Bottom Centered)
        date_str = now.strftime("%a, %d %b %Y")
        bbox2 = draw.textbbox((0,0), date_str, font=self.font_date)
        w2 = bbox2[2] - bbox2[0]
        x2 = (self.width - w2) // 2
        
        # Check if Stopwatch is active override
        if self.stopwatch_start > 0 or self.stopwatch_paused_at > 0:
             self._draw_stopwatch(draw)
        else:
             draw.text((x2, 32), date_str, font=self.font_date, fill=1)

        return img

    def _draw_stopwatch(self, draw):
        # Overlay stopwatch at bottom
        # Calculate time
        if self.is_running:
            elapsed = time.time() - self.stopwatch_start
        else:
            if self.stopwatch_paused_at > 0:
                elapsed = self.stopwatch_paused_at - self.stopwatch_start
            else:
                elapsed = 0
                
        # Format
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        hunc = int((elapsed * 100) % 100)
        
        sw_str = f"SW: {mins:02d}:{secs:02d}.{hunc:02d}"
        
        # Draw background bar to clear date
        draw.rectangle([0, 32, 160, 43], fill=0)
        draw.line([0, 31, 160, 31], fill=1)
        
        # Center
        bbox = draw.textbbox((0,0), sw_str, font=self.font_date)
        w = bbox[2] - bbox[0]
        x = (self.width - w) // 2
        draw.text((x, 32), sw_str, font=self.font_date, fill=1)

    def handle_input(self, btn_id):
        # Btn 1: Start/Pause
        # Btn 2: Reset
        if btn_id == 1:
            if self.is_running:
                # Pause
                self.stopwatch_paused_at = time.time()
                self.is_running = False
            else:
                # Start
                if self.stopwatch_paused_at > 0:
                    # Resume
                    pause_dur = time.time() - self.stopwatch_paused_at
                    self.stopwatch_start += pause_dur
                    self.stopwatch_paused_at = 0
                else:
                    # Fresh Start
                    if self.stopwatch_start == 0:
                        self.stopwatch_start = time.time()
                
                self.is_running = True
                
        elif btn_id == 2:
            # Reset
            self.is_running = False
            self.stopwatch_start = 0
            self.stopwatch_paused_at = 0
            
        return True
