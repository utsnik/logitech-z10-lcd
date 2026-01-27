from .base import BasePlugin
from PIL import Image, ImageDraw, ImageFont
import subprocess
import time
try:
    import win32api
    import win32con
except ImportError:
    win32api = None

class MediaPlugin(BasePlugin):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.name = "Media Info"
        try:
            self.font_large = ImageFont.truetype("arialbd.ttf", 12) # Larger per request
            self.font_small = ImageFont.truetype("arial.ttf", 10)
        except:
            self.font_large = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
        self.media_data = {"artist": "", "title": "No Media", "album": "", "pos": 0, "dur": 1}
        self.last_check = 0

    def get_track_info(self):
        if time.time() - self.last_check < 1.0:
            return
            
        try:
            cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", "get_media.ps1"]
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            output = subprocess.check_output(cmd, startupinfo=startupinfo).decode().strip()
            # Expect "Artist|Title|Album|Pos|Dur"
            parts = output.split('|')
            if len(parts) >= 5:
                self.media_data = {
                    "artist": parts[0],
                    "title": parts[1],
                    "album": parts[2],
                    "pos": int(parts[3]),
                    "dur": int(parts[4]) if int(parts[4]) > 0 else 1
                }
            else:
                self.media_data["title"] = output
        except:
            pass
        self.last_check = time.time()

    def update(self):
        img = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(img)
        
        self.get_track_info()
        data = self.media_data
        
        # 1. Title (Top)
        draw.text((2, -1), data['title'][:22], font=self.font_large, fill=1)
        
        # 2. Album (Middle - requested Album Name)
        info_str = f"{data['artist']}"
        if data['album']:
            info_str += f" - {data['album']}"
            
        if len(info_str) > 35: info_str = info_str[:35] + "..."
        draw.text((2, 13), info_str, font=self.font_small, fill=1)
        
        # 3. Progress Bar (Vertical Lines + Time on Right)
        # Layout: [ |========      | ]  1:23
        bar_x1, bar_x2 = 2, 115
        bar_y = 30
        
        # Start/End Markers
        draw.line([bar_x1, bar_y, bar_x1, bar_y+8], fill=1)     # Start |
        draw.line([bar_x2, bar_y, bar_x2, bar_y+8], fill=1)     # End |
        # Center Line (Track)
        draw.line([bar_x1, bar_y+4, bar_x2, bar_y+4], fill=1)
        
        # Fill Blob
        pct = data['pos'] / data['dur']
        if pct > 1.0: pct = 1.0
        
        # Draw a box for progress
        fill_width = int((bar_x2 - bar_x1) * pct)
        if fill_width > 0:
            # Solid rect
            draw.rectangle([bar_x1, bar_y+2, bar_x1 + fill_width, bar_y+6], fill=1)
        
        # Time Text (Right side)
        def fmt_time(s):
            m = s // 60
            s = s % 60
            return f"{m}:{s:02d}"
            
        # Only show current time to save space, or "Pos" if cramped
        t_str = fmt_time(data['pos'])
        draw.text((120, 27), t_str, font=self.font_large, fill=1)
            
        return img
    
    
    def handle_input(self, btn_id):
        # Media Controls
        # 1: Prev, 2: Next, 3: Play/Pause, 4: Stop?
        print(f"Media Button: {btn_id}")
        
        VK_MEDIA_NEXT_TRACK = 0xB0
        VK_MEDIA_PREV_TRACK = 0xB1
        VK_MEDIA_STOP = 0xB2
        VK_MEDIA_PLAY_PAUSE = 0xB3
        
        if btn_id == 1: # Prev
            self.send_media_key(VK_MEDIA_PREV_TRACK)
        elif btn_id == 2: # Next
            self.send_media_key(VK_MEDIA_NEXT_TRACK)
        elif btn_id == 3: # Play/Pause
            self.send_media_key(VK_MEDIA_PLAY_PAUSE)
        elif btn_id == 4: # Stop
            self.send_media_key(VK_MEDIA_STOP)
            
        return True

    def send_media_key(self, vk_code):
        if not win32api: return
        # Key Down
        win32api.keybd_event(vk_code, 0, 0, 0)
        # Key Up
        win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
