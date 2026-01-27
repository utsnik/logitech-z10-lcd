from .base import BasePlugin
from PIL import Image, ImageDraw, ImageFont
import subprocess
import time
import threading

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
            self.font_large = ImageFont.truetype("arialbd.ttf", 14)
            self.font_small = ImageFont.truetype("arial.ttf", 10)
        except:
            self.font_large = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            
        self.media_data = {"artist": "", "title": "No Media", "album": "", "pos": 0, "dur": 1}
        self.last_check = 0
        self.tick = 0
        
        # Async background fetcher
        self.is_fetching = False
        
    def get_track_info_async(self):
        """Threaded function to fetch media data without blocking UI"""
        if self.is_fetching:
            return
        self.is_fetching = True
        
        def _fetch():
            try:
                cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", "get_media.ps1"]
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                output = subprocess.check_output(cmd, startupinfo=startupinfo).decode().strip()
                parts = output.split('|')
                if len(parts) >= 5:
                    new_data = {
                        "artist": parts[0],
                        "title": parts[1],
                        "album": parts[2],
                        "pos": int(parts[3]),
                        "dur": int(parts[4]) if int(parts[4]) > 0 else 1
                    }
                    # Reset tick if track changed
                    if new_data["title"] != self.media_data["title"]:
                        # Note: self.tick isn't thread-safe but we just read/write small ints
                        self.tick = 0 
                    self.media_data = new_data
            except:
                pass
            finally:
                self.is_fetching = False
                self.last_check = time.time()

        thread = threading.Thread(target=_fetch, daemon=True)
        thread.start()

    def draw_scrolling_text(self, draw, text, y, font, limit_w):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        
        if tw <= limit_w:
            draw.text((2, y), text, font=font, fill=1)
            return

        total_scroll = tw - limit_w + 20
        
        if self.tick < 20: 
            scroll_x = 0
        elif self.tick < 20 + total_scroll:
            scroll_x = -(self.tick - 20)
        else:
            if self.tick > 20 + total_scroll + 20:
                self.tick = 0
            scroll_x = -total_scroll
            
        draw.text((2 + scroll_x, y), text, font=font, fill=1)

    def update(self):
        img = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(img)
        
        # Trigger async fetch every 1 second
        if time.time() - self.last_check > 1.0:
            self.get_track_info_async()
            
        self.tick += 1
        data = self.media_data
        
        # 1. Title
        self.draw_scrolling_text(draw, data['title'], -1, self.font_large, 115)
        
        # 2. Artist - Album
        info_str = f"{data['artist']}"
        if data['album']:
            info_str += f" - {data['album']}"
        self.draw_scrolling_text(draw, info_str, 15, self.font_small, 115)
        
        # 3. Progress Bar
        bar_x1, bar_x2 = 2, 115
        bar_y = 32
        draw.line([bar_x1, bar_y, bar_x1, bar_y+8], fill=1)
        draw.line([bar_x2, bar_y, bar_x2, bar_y+8], fill=1)
        draw.line([bar_x1, bar_y+4, bar_x2, bar_y+4], fill=1)
        
        pct = data['pos'] / data['dur']
        if pct > 1.0: pct = 1.0
        fill_width = int((bar_x2 - bar_x1) * pct)
        if fill_width > 0:
            draw.rectangle([bar_x1, bar_y+2, bar_x1 + fill_width, bar_y+6], fill=1)
        
        def fmt_time(s):
            m = s // 60
            s = s % 60
            return f"{m}:{s:02d}"
            
        t_str = fmt_time(data['pos'])
        draw.text((120, 27), t_str, font=self.font_large, fill=1)
            
        return img

    def handle_input(self, btn_id):
        # ... and media controls remain same ...
        VK_MEDIA_NEXT_TRACK = 0xB0
        VK_MEDIA_PREV_TRACK = 0xB1
        VK_MEDIA_STOP = 0xB2
        VK_MEDIA_PLAY_PAUSE = 0xB3
        
        if btn_id == 1: self.send_media_key(VK_MEDIA_PREV_TRACK)
        elif btn_id == 2: self.send_media_key(VK_MEDIA_NEXT_TRACK)
        elif btn_id == 3: self.send_media_key(VK_MEDIA_PLAY_PAUSE)
        elif btn_id == 4: self.send_media_key(VK_MEDIA_STOP)
        return True

    def send_media_key(self, vk_code):
        if not win32api: return
        win32api.keybd_event(vk_code, 0, 0, 0)
        win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
