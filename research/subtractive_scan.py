"""
Subtractive Scan for Z-10 LCD
Fills the screen with 0xFF and moves a 0x00 "gap" through the buffer.
This will help us see exactly where the pixels are mapped.
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
        print("Starting Subtractive Scan...")
        print("The screen should be Solid White, with a moving black 'glitch'.")
        
        # We start with ALL WHITE
        base_buffer = bytearray([REPORT_ID] + [0xFF] * 991)
        
        # Scan through the buffer in 10-byte chunks
        for offset in range(0, 991, 10):
            print(f"  Clearing segment starting at byte {offset}...")
            
            # Create a copy of the white buffer
            test_buffer = bytearray(base_buffer)
            
            # Set a 20-byte "gap" to 0x00
            for i in range(20):
                idx = 1 + offset + i
                if idx < 992:
                    test_buffer[idx] = 0x00
            
            dev.write(0x03, test_buffer, timeout=1000)
            time.sleep(0.3)
            
    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
