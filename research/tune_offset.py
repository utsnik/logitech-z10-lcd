"""
Z-10 Offset Tuner
-----------------
Use this to align the image perfectly.
We will draw a border around the screen. 
Adjust the offset until the border fits the screen exactly!

Controls:
 [A] Decrease Offset (-1 byte)
 [D] Increase Offset (+1 byte)
 
 [X] Exit

Last Value Sent will be printed on screen.
"""
import usb.core
import usb.util
import usb.backend.libusb1
import os
import time
import msvcrt
import threading
from PIL import Image, ImageDraw

VID = 0x046D
PID = 0x0A07
REPORT_ID = 0x03
WIDTH = 160
HEIGHT = 43

# Start around the user's guess
current_offset = 24 
keep_running = True

def input_drainer(dev):
    while keep_running:
        try:
            dev.read(0x83, 64, timeout=100)
        except:
            pass
        time.sleep(0.05)

def create_border_image():
    img = Image.new('1', (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(img)
    # Draw a box around the edges
    draw.rectangle([0, 0, WIDTH-1, HEIGHT-1], outline=1)
    # Draw an 'X' to see centering
    draw.line([0, 0, WIDTH-1, HEIGHT-1], fill=1)
    draw.line([0, HEIGHT-1, WIDTH-1, 0], fill=1)
    return img

def send_image(dev, img, offset):
    buffer = bytearray(992)
    buffer[0] = REPORT_ID
    
    # Pack bits
    pixels = img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if pixels[x, y]:
                idx = y * WIDTH + x
                byte_pos = 1 + offset + (idx // 8) # APPLY OFFSET HERE
                if byte_pos < 992:
                    bit_pos = 7 - (idx % 8)
                    buffer[byte_pos] |= (1 << bit_pos)
    try:
        dev.write(0x03, buffer, timeout=1000)
    except:
        pass

def main():
    global current_offset, keep_running
    
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
            
        # Wake up
        try:
             # Standard Features
             dev.ctrl_transfer(0x21, 0x09, 0x0301, 0x0002, [0x01]) # Contrast?
             dev.ctrl_transfer(0x21, 0x09, 0x0302, 0x0002, [0x02]) # Backlight?
             dev.ctrl_transfer(0x21, 0x09, 0x0303, 0x0002, [0x01]) # Mode?
             dev.ctrl_transfer(0x21, 0x09, 0x0304, 0x0002, [0xFF]) # ?
        except:
             pass

        # Start drainer
        t = threading.Thread(target=input_drainer, args=(dev,))
        t.daemon = True
        t.start()

        img = create_border_image()
        print("Offset Tuner Started.")
        print("Use A/D to move the image until the Border fits.")
        
        while keep_running:
            print(f"Current Offset: {current_offset}   ", end='\r')
            
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                if key == 'x': break
                elif key == 'a': 
                    current_offset = max(0, current_offset - 1)
                elif key == 'd': 
                    current_offset = min(100, current_offset + 1)
            
            send_image(dev, img, current_offset)
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        keep_running = False
        usb.util.dispose_resources(dev)
        print("\nDone.")

if __name__ == "__main__":
    main()
