"""
Core Driver for Logitech Z-10 LCD Display
Supports 160x43 monochrome bitmap rendering via PyUSB/WinUSB
Includes "Input Drainer" thread to prevent buffer lockups.
"""

import usb.core
import usb.util
import usb.backend.libusb1
import os
import threading
import time
from PIL import Image, ImageDraw, ImageFont

class Z10LCD:
    VID = 0x046D
    PID = 0x0A07
    WIDTH = 160
    HEIGHT = 43
    REPORT_ID = 0x03
    
    def __init__(self):
        self.dev = None
        self.backend = None
        self.thread = None
        self._input_thread_running = False
        self._setup_backend()
        
    def _setup_backend(self):
        # Use the directory of the script/module, not the CWD
        base_path = os.path.dirname(os.path.abspath(__file__))
        backend_path = os.path.join(base_path, "libusb-1.0.dll")
        if not os.path.exists(backend_path):
            raise FileNotFoundError(f"libusb-1.0.dll not found at {backend_path}")
        self.backend = usb.backend.libusb1.get_backend(find_library=lambda x: backend_path)

    def connect(self):
        self.dev = usb.core.find(idVendor=self.VID, idProduct=self.PID, backend=self.backend)
        if self.dev is None:
            raise ConnectionError("Z-10 speakers not found. Check USB connection and WinUSB driver.")
        
        try:
            # Try to detach kernel driver if on Linux (ignored on Windows)
            if self.dev.is_kernel_driver_active(2):
                self.dev.detach_kernel_driver(2)
        except:
            pass

        try:
            # Force reset the device to clear stale flags/locks
            print("Resetting USB Device...")
            self.dev.reset()
            time.sleep(0.5)
            # Re-find after reset
            self.dev = usb.core.find(idVendor=self.VID, idProduct=self.PID, backend=self.backend)
        except Exception as e:
            print(f"Reset Warning: {e}")

        try:
            self.dev.set_configuration()
        except usb.core.USBError:
            pass # Already configured
            
        # Explicitly claim Interface 2 (LCD) to prevent conflicts
        try:
            usb.util.claim_interface(self.dev, 2)
            print("Interface 2 claimed.")
        except usb.core.USBError as e:
            print(f"Warning: Could not claim interface 2: {e}")

        # Initialize Display (Wake Up / Backlight / Contrast)
        self._wake_up_display()
            
        # Start the Input Drainer
        self._start_input_drainer()
        
    def _wake_up_display(self):
        """Sends initialization 'Feature Reports' to wake up LCD and set Backlight."""
        # Based on successful brute-force from 'test_backlight_scan.py'
        # We send a sequence of likely commands for Contrast(0x01), Backlight(0x02), Mode(0x03)
        print("Initializing LCD (Sending Wake-Up Features)...")
        features = [0x01, 0x02, 0x03, 0x04]
        values = [0x01, 0x02, 0x10, 0xFF] # A mix of 'On', 'Medium', and 'High'
        
        for feat in features:
            for val in values:
                try:
                    # bmRequestType 0x21, bRequest 0x09 (Set Report), wValue (ReportType HighByte + ID), wIndex (Interface)
                    wValue = (0x03 << 8) | feat
                    self.dev.ctrl_transfer(0x21, 0x09, wValue, 0x0002, [val])
                except:
                    pass
        # Give it a moment to wake up
        time.sleep(0.2)

    def _start_input_drainer(self):
        """Starts a background thread to drain (and optionally process) Input Endpoint 0x83."""
        self._input_thread_running = True
        self.thread = threading.Thread(target=self._drain_inputs)
        self.thread.daemon = True
        self.thread.start()
        
    def set_input_callback(self, callback):
        """Sets a function to be called when input data is received."""
        self.input_callback = callback

    def _drain_inputs(self):
        self.input_callback = None
        while self._input_thread_running and self.dev:
            try:
                # Read from Input Endpoint 0x83 (Buttons/Vol)
                # Max packet 64 bytes.
                # The device sends packets when state changes (or sometimes periodically).
                data = self.dev.read(0x83, 64, timeout=100)
                if data and self.input_callback:
                    self.input_callback(list(data))
            except usb.core.USBError:
                pass # Timeout is normal
            except Exception as e:
                print(f"Input Error: {e}")
                # Do NOT break, just continue to next packet. 
                # Otherwise a plugin crash kills the buttons.
                time.sleep(0.1)
                continue
            time.sleep(0.05)
            
    def disconnect(self):
        self._input_thread_running = False
        if self.dev:
            try:
                usb.util.release_interface(self.dev, 2)
            except:
                pass
            usb.util.dispose_resources(self.dev)
            self.dev = None

    def display_image(self, pil_image):
        """
        Converts a PIL image to the Z-10 LCD format and sends it.
        Format: Vertical Byte Packing (Nokia 5110 style) at Offset 24.
        """
        if self.dev is None:
            return

        if pil_image.mode != '1':
            pil_image = pil_image.convert('1')
        
        if pil_image.size != (self.WIDTH, self.HEIGHT):
            pil_image = pil_image.resize((self.WIDTH, self.HEIGHT))

        OFFSET = 32 # Shifted to standard 0x20 (32) to fix left-cropping
        
        # Prepare buffer
        buffer = bytearray(992)
        buffer[0] = self.REPORT_ID
        
        # Pack bits (Vertical Style)
        # We iterate across columns (x), then down pages (y / 8)
        pixels = pil_image.load()
        ptr = 1 + OFFSET
        
        for y_page in range(0, self.HEIGHT, 8):
            for x in range(self.WIDTH):
                # Mask Right Edge (x=159) to prevent buffer wrap-around artifacts
                if x >= 159:
                    ptr += 1
                    continue

                byte_val = 0
                for bit in range(8):
                    y = y_page + bit
                    if y < self.HEIGHT and pixels[x, y]:
                        # 0 = Black, 255 = White. In mode '1', non-zero is usually white.
                        byte_val |= (1 << bit)
                
                if ptr < 992:
                    buffer[ptr] = byte_val
                    ptr += 1

        # Write to Endpoint 0x03
        self.dev.write(0x03, buffer, timeout=1000)

    def clear(self):
        img = Image.new('1', (self.WIDTH, self.HEIGHT), 0)
        self.display_image(img)

# Helper for creating layout
def create_canvas():
    return Image.new('1', (160, 43), 0)

if __name__ == "__main__":
    # Internal test
    lcd = Z10LCD()
    try:
        lcd.connect()
        print("Connected to Z-10!")
        
        canvas = create_canvas()
        draw = ImageDraw.Draw(canvas)
        
        # Draw some test patterns
        draw.rectangle([0, 0, 159, 42], outline=1)
        draw.text((10, 10), "Z-10 PYTHON DRIVER", fill=1)
        draw.line([0, 25, 159, 25], fill=1)
        draw.text((20, 30), "SUCCESS! LCD WORKING", fill=1)
        
        lcd.display_image(canvas)
        print("Sent test image to LCD")
        
        # Keep alive for testing
        print("Keeping open for 10 seconds...")
        time.sleep(10)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        lcd.disconnect()
