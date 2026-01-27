"""
Full Pattern Test for Z-10
Fills the entire 991-byte data buffer with a recognizable pattern
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
        print("Sending full-buffer pattern (0xAA/0x55)...")
        
        # We fill EVERY byte of the 991-byte data section
        # buffer[0] is ID 0x03
        # buffer[1-991] is data
        buffer = bytearray([REPORT_ID] + ([0xAA, 0x55] * 495) + [0xAA])
        
        # We'll send it a few times to ensure it's "caught" by the firmware
        for i in range(5):
            dev.write(0x03, buffer, timeout=1000)
            print(f"  [{i+1}] Sent")
            time.sleep(0.5)
            
        print("Check LCD. It should show a fine checkerboard/stripes over the whole screen.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
