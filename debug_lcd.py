import usb.core
import usb.util
import usb.backend.libusb1
import os
import time
from PIL import Image, ImageDraw

# Minimal Driver extraction
class DebugLCD:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        backend_path = os.path.join(base_path, "libusb-1.0.dll")
        self.backend = usb.backend.libusb1.get_backend(find_library=lambda x: backend_path)
        self.dev = None

    def log(self, msg):
        with open("debug_log.txt", "a") as f:
            f.write(str(msg) + "\n")

    def connect(self):
        self.log("Finding Device...")
        self.dev = usb.core.find(idVendor=0x046D, idProduct=0x0A07, backend=self.backend)
        if not self.dev:
            self.log("ERROR: Device Not Found!")
            return False
        
        self.log(f"Device Found: {self.dev}")
        
        try:
            if self.dev.is_kernel_driver_active(2):
                self.dev.detach_kernel_driver(2)
        except: pass
        
        self.log("Resetting...")
        self.dev.reset()
        time.sleep(1)
        self.dev = usb.core.find(idVendor=0x046D, idProduct=0x0A07, backend=self.backend)
        self.dev.set_configuration()
        usb.util.claim_interface(self.dev, 2)
        self.log("Interface Claimed.")
        return True

    def wake_up(self):
        self.log("Sending Wake Up Signal...")
        # Cycle through known initialization commands
        # 0x03 report type is Feature
        try:
            # Contrast
            self.dev.ctrl_transfer(0x21, 0x09, 0x0301, 2, [0x01]) 
            # Backlight On
            self.dev.ctrl_transfer(0x21, 0x09, 0x0302, 2, [0x02]) 
        except Exception as e:
            self.log(f"Wakeup error: {e}")

    def draw(self):
        self.log("Drawing Test Pattern...")
        img = Image.new('1', (160, 43), 0)
        draw = ImageDraw.Draw(img)
        # White background, Black Text
        draw.rectangle([0,0,160,43], fill=1)
        draw.text((10, 10), "DEBUG MODE", fill=0)
        draw.line([0,0,160,43], fill=0)
        
        # Send
        buffer = bytearray(992)
        buffer[0] = 0x03
        
        pixels = img.load()
        ptr = 1 + 32
        for y_page in range(0, 43, 8):
            for x in range(160):
                byte_val = 0
                for bit in range(8):
                    y = y_page + bit
                    if y < 43 and pixels[x, y]:
                        byte_val |= (1 << bit)
                if ptr < 992:
                    buffer[ptr] = byte_val
                    ptr += 1
        
        self.dev.write(0x03, buffer)
        print("Frame Sent.")

if __name__ == "__main__":
    lcd = DebugLCD()
    if lcd.connect():
        lcd.wake_up()
        while True:
            lcd.draw()
            time.sleep(1)
