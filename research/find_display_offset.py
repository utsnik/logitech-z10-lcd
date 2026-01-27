"""
Z-10 Offset Finder
------------------
The "Sliding Window" test worked, which means the LCD data doesn't start at Byte 0.
This script tries specific common offsets to find the right one.
"""
import usb.core
import usb.util
import usb.backend.libusb1
import os
import time

VID = 0x046D
PID = 0x0A07
REPORT_ID = 0x03

# Common Logitech LCD offsets
OFFSETS = [0, 32, 256, 1, 2, 4, 8, 16, 64]

def main():
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

        print("Testing Offsets... Watch the screen!")
        
        # 1. Clear Screen first
        empty = bytearray([REPORT_ID] + [0x00] * 991)
        try:
            dev.write(0x03, empty, timeout=1000)
        except:
             pass
        time.sleep(1)

        # 2. Test Offsets
        for offset in range(0, 200, 1): # Scan byte-by-byte for the first 200 bytes
            print(f"Testing Offset: {offset}")
            
            buffer = bytearray(empty)
            
            # Write a solid block of 100 bytes (pixels) at the offset
            # 100 bytes * 8 bits = 800 pixels (should fill about 5 rows)
            for i in range(100):
                target_idx = 1 + offset + i
                if target_idx < 992:
                    buffer[target_idx] = 0xFF
            
            try:
                dev.write(0x03, buffer, timeout=1000)
            except Exception as e:
                print(f"Error: {e}")
            
            # Speed up the visual scan
            time.sleep(0.05) 

        print("\nDid you see a white block moving?")
        print("Now trying specific G15 offsets slowly...")
        
        for offset in [0, 32]:
            print(f"Holding Offset {offset} for 3 seconds...")
            buffer = bytearray(empty)
            # Fill entire screen worth of data (860 bytes)
            for i in range(860):
                 if 1 + offset + i < 992:
                      buffer[1 + offset + i] = 0xFF
            
            dev.write(0x03, buffer, timeout=1000)
            time.sleep(3)

    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
