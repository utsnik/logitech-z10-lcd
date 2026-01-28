from .base import BasePlugin
from PIL import Image, ImageDraw, ImageFont
import mmap
import ctypes
import struct
import time

# RTSS Shared Memory Structure Definition
# Based on RTSSSharedMemory.h from SDK
class RTSS_SHARED_MEMORY_V2(ctypes.Structure):
    _fields_ = [
        ("dwSignature", ctypes.c_uint32),
        ("dwVersion", ctypes.c_uint32),
        ("dwAppEntrySize", ctypes.c_uint32),
        ("dwAppArrOffset", ctypes.c_uint32),
        ("dwAppArrSize", ctypes.c_uint32),
        ("dwOSDEntrySize", ctypes.c_uint32),
        ("dwOSDArrOffset", ctypes.c_uint32),
        ("dwOSDArrSize", ctypes.c_uint32),
        ("dwOSDFrame", ctypes.c_uint32)
    ]

class RTSS_APP_ENTRY_V2(ctypes.Structure):
    _fields_ = [
        ("dwProcessId", ctypes.c_uint32),
        ("szName", ctypes.c_char * 260),
        ("dwFlags", ctypes.c_uint32),
        ("dwTime0", ctypes.c_uint32),
        ("dwTime1", ctypes.c_uint32),
        ("dwFrames", ctypes.c_uint32),
        ("dwFrameTime", ctypes.c_uint32),
        ("dwStatFlags", ctypes.c_uint32), # 2.7+
        ("dwStatTime0", ctypes.c_uint32),
        ("dwStatTime1", ctypes.c_uint32),
        ("dwStatFrames", ctypes.c_uint32),
        ("dwStatCount", ctypes.c_uint32),
        ("dwStatFrametimeMin", ctypes.c_uint32),
        ("dwStatFrametimeAvg", ctypes.c_uint32),
        ("dwStatFrametimeMax", ctypes.c_uint32),
        ("dwOSDX", ctypes.c_uint32),
        ("dwOSDY", ctypes.c_uint32),
        ("dwOSDPixelScale", ctypes.c_uint32),
    ]

class GamePlugin(BasePlugin):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.name = "Game Stats"
        try:
            self.font_vals = ImageFont.truetype("arialbd.ttf", 24)
            self.font_label = ImageFont.truetype("arial.ttf", 10)
        except:
            self.font_vals = ImageFont.load_default()
            self.font_label = ImageFont.load_default()
            
        self.last_map_open_time = 0
        self.map_file = None
        self.has_rtss = False
        
        # Persistence
        self.last_valid_app = None
        self.last_valid_time = 0

    def _open_map(self):
        if time.time() - self.last_map_open_time < 5:
            return # Don't spam open retry
            
        self.last_map_open_time = time.time()
        try:
            # Step 1: Map just the header (safe size) to read dimensions
            tmp = mmap.mmap(0, 1024, "RTSSSharedMemoryV2")
            
            from ctypes import sizeof
            header_buf = tmp.read(sizeof(RTSS_SHARED_MEMORY_V2))
            header = RTSS_SHARED_MEMORY_V2.from_buffer_copy(header_buf)
            
            # Calculate total needed size
            # Data layout can vary. We need the max extent.
            app_end = header.dwAppArrOffset + (header.dwAppArrSize * header.dwAppEntrySize)
            osd_end = header.dwOSDArrOffset + (header.dwOSDArrSize * header.dwOSDEntrySize)
            
            total_size = max(app_end, osd_end)
            
            # Sanity check size
            if total_size < 1024: total_size = 65536 # Default fallback
            if total_size > 1024 * 1024 * 64: total_size = 1024 * 1024 * 64 # Cap at 64MB

            tmp.close()
            
            # Step 2: Map the actual full size
            self.map_file = mmap.mmap(0, total_size, "RTSSSharedMemoryV2")
            self.has_rtss = True
            # print(f"DEBUG: RTSS Connected! Size: {total_size}")
            
        except Exception as e:
            self.last_error = e
            # print(f"DEBUG: RTSS Open Failed: {e}")
            self.has_rtss = False
            self.map_file = None

    def update(self):
        if not self.map_file:
            self._open_map()

        img = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(img)

        # Draw Header
        draw.text((2, 0), "FPS MONITOR", font=self.font_label, fill=1)
        draw.line((0, 12, 160, 12), fill=1)

        if not self.has_rtss:
             err = getattr(self, 'last_error', 'RTSS Not Found')
             draw.text((10, 20), str(err)[:25], font=self.font_label, fill=1)
             return img

        try:
            self.map_file.seek(0)
            header_buf = self.map_file.read(ctypes.sizeof(RTSS_SHARED_MEMORY_V2))
            header = RTSS_SHARED_MEMORY_V2.from_buffer_copy(header_buf)
            
            # Signature "RTSS" = 0x53535452
            # Signature "RTSS"
            # Found on user system: 0x52545353 (Reverse endian?)
            # Standard SDK says: 0x53535452
            if header.dwSignature != 0x53535452 and header.dwSignature != 0x52545353:
                draw.text((10, 20), f"Bad Sig: {header.dwSignature:x}", font=self.font_label, fill=1)
                return img
                
            # Iterate Apps to find foreground 3D app
            # For simplicity, we just take the first active one that has frames > 0
            # or simply the one RTSS considers "foreground" which is usually index 0 in the array?
            # Actually RTSS sorts them. The one with dwFlags & 0x4 (OSD_FOREGROUND) is what we want.
            
            found_app = None
            
            # Iterate Apps to find foreground 3D app
            # Logic: Find the active app (Frames > 0) with the MOST RECENT update time (dwTime1)
            
            found_app = None
            last_update_time = 0
            
            for i in range(header.dwAppArrSize):
                offset = header.dwAppArrOffset + (i * header.dwAppEntrySize)
                self.map_file.seek(offset)
                entry_buf = self.map_file.read(ctypes.sizeof(RTSS_APP_ENTRY_V2))
                app = RTSS_APP_ENTRY_V2.from_buffer_copy(entry_buf)
                
                if app.dwProcessId == 0: continue
                
                # Clean Process Name
                name = app.szName.decode('utf-8', errors='ignore').split(chr(0))[0]
                
                # Filter out known background/overlay apps
                IGNORE_LIST = ["Overlay", "Launcher", "FrameView", "Steam", "FvContainer", "SearchApp", "ShellExperienceHost"]
                if any(x.lower() in name.lower() for x in IGNORE_LIST):
                    continue

                # Valid App if it has an update timestamp
                if app.dwTime1 > 0:
                     if app.dwTime1 > last_update_time:
                         found_app = app
                         last_update_time = app.dwTime1
            
            # Persistence Logic (Grace Period)
            if found_app:
                self.last_valid_app = found_app
                self.last_valid_time = time.time()
            elif self.last_valid_app and (time.time() - self.last_valid_time < 3.0):
                # Keep showing last app for 3 seconds if signal drops (e.g. alt-tab)
                found_app = self.last_valid_app

            if found_app:
                # Calculate FPS: 1,000,000 / FrameTime(us)
                fps = 0
                if found_app.dwFrameTime > 0:
                    fps = int(1000000 / found_app.dwFrameTime)
                
                draw.text((5, 15), f"{fps}", font=self.font_vals, fill=1)
                draw.text((50, 28), "FPS", font=self.font_label, fill=1)
                
                # Frametime
                ft = found_app.dwFrameTime / 1000.0
                draw.text((80, 15), f"{ft:.1f}ms", font=self.font_label, fill=1)
                
                # App Name
                name = found_app.szName.decode('utf-8', errors='ignore').split(chr(0))[0]
                if '\\' in name:
                    name = name.split('\\')[-1]
                name = name.replace(".exe", "").replace(".EXE", "")
                
                draw.text((80, 28), name[:15], font=self.font_label, fill=1)
                
            else:
                draw.text((10, 20), "No 3D App Active", font=self.font_label, fill=1)

        except Exception as e:
            self.last_error = f"ReadErr: {e}"
            # draw.text((10, 20), "Read Error", font=self.font_label, fill=1) # Let next frame show it
            self.has_rtss = False # Trigger re-open attempt
            self.map_file = None

        return img

    def handle_input(self, btn_id):
        return True
