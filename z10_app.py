"""
Z-10 Plugin Engine
------------------
Main application that runs the LCD.
Handles:
1. Driver Connection
2. Plugin Management
3. Button Input Routing
"""
import time
import sys
import os
import threading
try:
    import pystray
    from pystray import MenuItem as item
except ImportError:
    pystray = None

from z10_driver import Z10LCD
from plugins.monitor_plugin import MonitorPlugin
from plugins.system_expanded import EnhancedMonitorPlugin
from plugins.media_plugin import MediaPlugin
from plugins.input_debug import DebugPlugin

class Z10App:
    def __init__(self):
        self.lcd = Z10LCD()
        # Load Plugins
        self.plugins = [
            MonitorPlugin(160, 43),
            EnhancedMonitorPlugin(160, 43),
            MediaPlugin(160, 43)
        ]
        self.current_plugin_idx = 0
        self.running = True
        self.last_press_time = 0
        self.display_btn_hold_start = 0
        
        # Start Tray Icon
        if pystray:
            self.tray_thread = threading.Thread(target=self._setup_tray, daemon=True)
            self.tray_thread.start()

    def _setup_tray(self):
        try:
            from PIL import Image, ImageDraw
            # Create a simple icon
            icon_img = Image.new('RGB', (64, 64), color=(30, 30, 30))
            d = ImageDraw.Draw(icon_img)
            # Draw a stylistic 'Z'
            d.rectangle([10, 10, 54, 54], outline=(255, 165, 0), width=3)
            d.text((20, 15), "Z", fill=(255, 255, 255))
            
            def on_quit(icon, item):
                print("Exit via Tray Menu")
                self.running = False
                icon.stop()

            menu = pystray.Menu(item('Quit Z-10 App', on_quit))
            self.icon = pystray.Icon("Z10LCD", icon_img, "Logitech Z-10 LCD Driver", menu)
            self.icon.run()
        except Exception as e:
            print(f"Tray Icon Error: {e}")        
    def start(self):
        print("Starting Z-10 App...")
        
        while self.running:
            # 1. Connection Loop
            while not self.lcd.dev and self.running:
                try:
                    print("Connecting to Z-10...")
                    self.lcd.connect()
                    self.lcd.set_input_callback(self.on_input)
                    print("Connected!")
                except Exception as e:
                    # Check for "No Backend" (Missing Driver)
                    err_str = str(e)
                    if "No backend available" in err_str or "libusb" in err_str:
                        print("DRIVER MISSING! Launching Zadig...")
                        import subprocess
                        import ctypes
                        
                        # Show Alert
                        ctypes.windll.user32.MessageBoxW(0, 
                            "The Z-10 Driver is missing!\n\n"
                            "1. Zadig will now open.\n"
                            "2. Select 'Options -> List All Devices'.\n"
                            "3. Select 'Logitech Z-10 USB Speaker (Interface 2)'.\n"
                            "4. Click 'Replace Driver'.\n\n"
                            "The app will close. Restart it after installing.", 
                            "Z-10 Driver Setup", 0x40 | 0x1)
                        
                        # Launch Zadig if present
                        if os.path.exists("zadig.exe"):
                            subprocess.Popen("zadig.exe")
                        else:
                            ctypes.windll.user32.MessageBoxW(0, "Could not find zadig.exe to auto-install.", "Error", 0x10)
                        
                        sys.exit(0)

                    print(f"Waiting for device... ({e})")
                    time.sleep(3)
            
            # 2. Main Loop
            try:
                if self.lcd.dev:
                    plugin = self.plugins[self.current_plugin_idx]
                    img = plugin.update()
                    if img:
                        self.lcd.display_image(img)
                    time.sleep(0.1) # Faster loop for scrolling (10 FPS)
            except Exception as e:
                print(f"Device Error: {e}")
                self.lcd.disconnect() # Reset driver state
                time.sleep(1) # Wait before retry
                
    def stop(self):
        self.running = False
        if hasattr(self, 'icon'):
            self.icon.stop()
        self.lcd.disconnect()

    def on_input(self, data):
        """
        Handles raw input events.
        Display (Index 8): Switch Plugin (Short press), Exit (Long press 2s)
        Btns 1-4 (Index 2-5): Send to current Plugin
        """
        if len(data) <= 8:
            return

        # 1. Long-press Exit Logic (Display Button)
        is_display_pressed = (data[8] == 0x80)
        
        if is_display_pressed:
            if self.display_btn_hold_start == 0:
                self.display_btn_hold_start = time.time()
            else:
                if time.time() - self.display_btn_hold_start > 2.0:
                    print("!!! Long Press Detected: Exiting App !!!")
                    self.stop()
                    sys.exit(0)
            return # Don't process other buttons while Display is held
        else:
            # Button released - was it a short press?
            if self.display_btn_hold_start > 0:
                hold_duration = time.time() - self.display_btn_hold_start
                self.display_btn_hold_start = 0 # Reset
                if hold_duration < 1.0:
                    print("Display Button: Short Press -> Next Plugin")
                    self.next_plugin()
                return # Don't process other buttons on the same frame as a release

        # 2. Plugin Inputs (Debounced)
        if time.time() - self.last_press_time < 0.25:
            return

        btn_pressed = None
        if data[2] == 0x80: btn_pressed = 1
        elif data[3] == 0x80: btn_pressed = 2
        elif data[4] == 0x80: btn_pressed = 3
        elif data[5] == 0x80: btn_pressed = 4
        
        if btn_pressed:
            self.last_press_time = time.time()
            print(f"-> App: Sending Button {btn_pressed} to Plugin '{self.plugins[self.current_plugin_idx].name}'")
            self.plugins[self.current_plugin_idx].handle_input(btn_pressed)
    def next_plugin(self):
        self.current_plugin_idx = (self.current_plugin_idx + 1) % len(self.plugins)
        # Show overlay or print
        print(f"Switching to: {self.plugins[self.current_plugin_idx].name}")

if __name__ == "__main__":
    app = Z10App()
    app.start()
