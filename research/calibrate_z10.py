"""
Z-10 LCD Calibrator
-------------------
Use this to find the correct Contrast/Brightness settings.
The screen currently shows a CHECKERBOARD pattern.

Controls:
 [Q] Decrease Contrast (Feature 0x01)
 [W] Increase Contrast
 
 [A] Decrease Backlight (Feature 0x02)
 [S] Increase Backlight
 
 [Z] Toggle Inversion (Black/White swap)
 
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

VID = 0x046D
PID = 0x0A07
REPORT_ID = 0x03

# Initial Values (Mid-range guess)
current_contrast = 0x80 # 128
current_backlight = 0x02 # Medium
inverted = False
keep_running = True

def send_feature(dev, feat_id, val):
    try:
        wValue = (0x03 << 8) | feat_id
        dev.ctrl_transfer(0x21, 0x09, wValue, 0x0002, [val])
    except:
        pass

def input_drainer(dev):
    while keep_running:
        try:
            dev.read(0x83, 64, timeout=100)
        except:
            pass
        time.sleep(0.05)

def main():
    global current_contrast, current_backlight, inverted, keep_running
    
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

        # Start drainer
        t = threading.Thread(target=input_drainer, args=(dev,))
        t.daemon = True
        t.start()

        print("Calibrator Started.")
        print("Press Q/W to change Contrast. A/S for Backlight.")
        
        # Initial Set
        send_feature(dev, 0x01, current_contrast)
        send_feature(dev, 0x02, current_backlight)
        send_feature(dev, 0x03, 0x00) # Mode?
        
        while keep_running:
            # Handle Keys
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                if key == 'x': break
                elif key == 'q': 
                    current_contrast = max(0, current_contrast - 16)
                    send_feature(dev, 0x01, current_contrast)
                elif key == 'w': 
                    current_contrast = min(255, current_contrast + 16)
                    send_feature(dev, 0x01, current_contrast)
                elif key == 'a': 
                    current_backlight = max(0, current_backlight - 1)
                    send_feature(dev, 0x02, current_backlight)
                elif key == 's': 
                    current_backlight = min(255, current_backlight + 1)
                    send_feature(dev, 0x02, current_backlight)
                elif key == 'z':
                    inverted = not inverted
                
                print(f"Contrast: {hex(current_contrast)} | Backlight: {hex(current_backlight)} | Inv: {inverted}   ", end='\r')

            # Send Checkerboard Pattern
            buffer = bytearray(992)
            buffer[0] = REPORT_ID
            fill = 0xAA if not inverted else 0x55
            for i in range(1, 992):
                buffer[i] = fill
            
            try:
                dev.write(0x03, buffer, timeout=1000)
            except:
                pass
            
            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        keep_running = False
        usb.util.dispose_resources(dev)
        print("\nDone.")

if __name__ == "__main__":
    main()
