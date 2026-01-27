"""
Offset Discovery Test for Z-10 LCD
Tests if the visible data starts after a padding (e.g. 131 bytes).
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
        
        # Test 1: Fill only the LAST 860 bytes (guessing 131 bytes padding at start)
        print("Test 1: Filling LAST 860 bytes (Padding at START) - Wait 5s")
        buffer = bytearray([REPORT_ID] + [0x00] * 131 + [0xFF] * 860)
        dev.write(0x03, buffer, timeout=1000)
        time.sleep(5)
        
        # Test 2: Fill only the FIRST 860 bytes (Padding at END)
        print("Test 2: Filling FIRST 860 bytes (Padding at END) - Wait 5s")
        buffer = bytearray([REPORT_ID] + [0xFF] * 860 + [0x00] * 131)
        dev.write(0x03, buffer, timeout=1000)
        time.sleep(5)
        
        # Test 3: Sliding window of 100 bytes - watch when it appears
        print("Test 3: Sliding 100-byte window (Watch screen for any movement!)")
        for offset in range(0, 900, 50):
            print(f"  Window at offset {offset}")
            buffer = bytearray([REPORT_ID] + [0x00] * 991)
            for i in range(100):
                if offset + i < 991:
                    buffer[1 + offset + i] = 0xFF
            dev.write(0x03, buffer, timeout=1000)
            time.sleep(0.5)
            
    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
