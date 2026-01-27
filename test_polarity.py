"""
Polarity Test for Z-10
The logo is gone (Good!). Now we find the pixels.
Alternates between 0x00 and 0xFF to see which one lights up.
"""
import usb.core
import usb.util
import usb.backend.libusb1
import os
import time

VID = 0x046D
PID = 0x0A07
REPORT_ID = 0x03

def main():
    backend_path = os.path.join(os.getcwd(), "libusb-1.0.dll")
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: backend_path)
    dev = usb.core.find(idVendor=VID, idProduct=PID, backend=backend)
    
    if dev is None:
        print("Device not found")
        return

    try:
        dev.set_configuration()
        print("Logo is gone! Now testing which value = 'Pixel On'...")
        
        while True:
            # 1. Send ALL 0x00 (Usually 'Off')
            print("Sending 0x00 (All Zero)...")
            payload = bytearray([REPORT_ID] + [0x00] * 991)
            dev.write(0x03, payload, timeout=1000)
            time.sleep(2)
            
            # 2. Send ALL 0xFF (Usually 'On')
            print("Sending 0xFF (All One)...")
            payload = bytearray([REPORT_ID] + [0xFF] * 991)
            dev.write(0x03, payload, timeout=1000)
            time.sleep(2)
            
            # 3. Send Checkerboard
            print("Sending Checkerboard (0xAA)...")
            payload = bytearray([REPORT_ID] + [0xAA] * 991)
            dev.write(0x03, payload, timeout=1000)
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
