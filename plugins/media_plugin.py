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
            
        self.media_data = {"artist": "", "title": "No Media", "album": "", "pos": 0, "dur": 1, "status": "Closed"}
        self.last_check_time = 0
        self.last_sync_time = 0 # System time of last real data fetch
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
                        "dur": int(parts[4]) if int(parts[4]) > 0 else 1,
                        "status": parts[5] if len(parts) > 5 else "Playing" # Assuming PS script might send status
                    }
                    
                    # If track changed or seeking happened, reset our local timer sync
                    if new_data["title"] != self.media_data["title"] or abs(new_data["pos"] - self.media_data["pos"]) > 2:
                        self.tick = 0 
                    
                    self.media_data = new_data
                    self.last_sync_time = time.time()
            except:
                pass
            finally:
                self.is_fetching = False
                self.last_check_time = time.time()

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
        
        # 1. Sync data (Throttled Background Fetch)
        if time.time() - self.last_check_time > 1.5: # Increased to 1.5s to give PS more breathing room
            self.get_track_info_async()
            
        self.tick += 1
        data = self.media_data
        
        # 2. Timer Interpolation
        # Calculate how many seconds have passed since the last REAL sync from PowerShell
        render_pos = data['pos']
        if self.last_sync_time > 0:
            elapsed_since_sync = time.time() - self.last_sync_time
            # Only interpolate if we aren't paused (best guess)
            render_pos = data['pos'] + int(elapsed_since_sync)
            if render_pos > data['dur']: render_pos = data['dur']

        # 3. Title (Scrolling)
        self.draw_scrolling_text(draw, data['title'], -1, self.font_large, 115)
        
        # 4. Artist - Album (Scrolling)
        info_str = f"{data['artist']}"
        if data['album']:
            info_str += f" - {data['album']}"
        self.draw_scrolling_text(draw, info_str, 15, self.font_small, 115)
        
        # 5. Progress Bar
        bar_x1, bar_x2 = 2, 115
        bar_y = 32
        draw.line([bar_x1, bar_y, bar_x1, bar_y+8], fill=1)
        draw.line([bar_x2, bar_y, bar_x2, bar_y+8], fill=1)
        draw.line([bar_x1, bar_y+4, bar_x2, bar_y+4], fill=1)
        
        pct = render_pos / data['dur']
        if pct > 1.0: pct = 1.0
        fill_width = int((bar_x2 - bar_x1) * pct)
        if fill_width > 0:
            draw.rectangle([bar_x1, bar_y+2, bar_x1 + fill_width, bar_y+6], fill=1)
        
        def fmt_time(s):
            m = s // 60
            s = s % 60
            f_s = f"{m}:{s:02d}"
            return f_s
            
        t_str = fmt_time(render_pos)
        draw.text((120, 27), t_str, font=self.font_large, fill=1)
            
        return img

    def handle_input(self, btn_id):
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
