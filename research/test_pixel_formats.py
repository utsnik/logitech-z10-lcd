"""
Z-10 Pixel Format Tester (Robust)
---------------------------------
Testing 3 pixel packing formats at Offset 24.
Includes Input Drainer and explicit Interface Claiming to prevent crashes/locks.
"""
import usb.core
import usb.util
import usb.backend.libusb1
import os
import time
import threading
from PIL import Image, ImageDraw, ImageFont

VID = 0x046D
PID = 0x0A07
REPORT_ID = 0x03
WIDTH = 160
HEIGHT = 43
OFFSET = 24 

keep_running = True

def input_drainer(dev):
    """Keeps the device happy by draining button events."""
    while keep_running:
        try:
            dev.read(0x83, 64, timeout=100)
        except:
            pass
        time.sleep(0.05)

def send_horizontal(dev, img, reverse_bits=False):
    buffer = bytearray(992)
    buffer[0] = REPORT_ID
    pixels = img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if pixels[x, y]:
                idx = y * WIDTH + x
                byte_pos = 1 + OFFSET + (idx // 8)
                if byte_pos < 992:
                    bit_pos = (idx % 8) if reverse_bits else (7 - (idx % 8))
                    buffer[byte_pos] |= (1 << bit_pos)
    try:
        dev.write(0x03, buffer, timeout=1000)
    except Exception as e:
        print(f"Write Error (Horiz): {e}")

def send_vertical(dev, img):
    # Nokia 5110 / SSD1306 style: Each byte is a vertical column of 8 pixels
    buffer = bytearray(992)
    buffer[0] = REPORT_ID
    pixels = img.load()
    
    ptr = 1 + OFFSET
    
    # We iterate across columns (x), then down pages (y / 8)
    for y_page in range(0, HEIGHT, 8):
        for x in range(WIDTH):
            byte_val = 0
            for bit in range(8):
                y = y_page + bit
                if y < HEIGHT and pixels[x, y]:
                    byte_val |= (1 << bit)
            
            if ptr < 992:
                buffer[ptr] = byte_val
                ptr += 1
                
    try:
        dev.write(0x03, buffer, timeout=1000)
    except Exception as e:
        print(f"Write Error (Vert): {e}")

def main():
    global keep_running
    
    backend_path = os.path.join(os.getcwd(), "libusb-1.0.dll")
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: backend_path)
    dev = usb.core.find(idVendor=VID, idProduct=PID, backend=backend)
    
    if dev is None:
        print("Device not found")
        return

    try:
        dev.set_configuration()
        try:
             usb.util.claim_interface(dev, 2)
        except:
             pass
        
        # Start Input Drainer (Crucial for stability)
        t = threading.Thread(target=input_drainer, args=(dev,))
        t.daemon = True
        t.start()

        # Wake Up Sequence
        try:
             dev.ctrl_transfer(0x21, 0x09, 0x0301, 0x0002, [0x01])
             dev.ctrl_transfer(0x21, 0x09, 0x0302, 0x0002, [0x02])
             dev.ctrl_transfer(0x21, 0x09, 0x0303, 0x0002, [0x01])
        except:
             pass

        # Create Test Image
        img = Image.new('1', (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(img)
        # Big text
        try:
            # Try a default font, or load one if possible. 
            # Default is very small. Let's draw shapes too.
            draw.text((10, 5), "Z-10 TEST", fill=1)
        except:
            pass
            
        draw.rectangle([0, 0, 40, 40], outline=1)
        draw.line([0,0, 40,40], fill=1)
        draw.ellipse([50, 0, 90, 40], outline=1)

        print("Testing Formats at Offset 24...")
        
        while True:
            print("1. Standard Horizontal (Current)...")
            send_horizontal(dev, img, reverse_bits=False)
            time.sleep(4)
            
            print("2. Horizontal (Reversed Bits)...")
            send_horizontal(dev, img, reverse_bits=True)
            time.sleep(4)
            
            print("3. Vertical Byte Packing (Nokia style)...")
            send_vertical(dev, img)
            time.sleep(4)

    except KeyboardInterrupt:
        pass
    finally:
        keep_running = False
        if dev:
            try:
                usb.util.release_interface(dev, 2)
            except:
                pass
            usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
