"""
Diagnostic Pattern for Z-10 LCD
Sends a 50/50 horizontal split to determine bit orientation.
"""
import usb.core
import usb.util
import usb.backend.libusb1
import os

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

    # Buffer: 1 byte Report ID + 991 bytes 
    buffer = bytearray([REPORT_ID] + [0x00] * 991)
    
    # Let's fill exactly the first 430 bytes with 0xFF.
    # If the screen is row-major, this should fill roughly the top half.
    # 160 pixels * 21.5 rows = 3440 pixels = 430 bytes.
    for i in range(1, 431):
        buffer[i] = 0xFF
        
    print("Sending Horizontal Split Pattern (Top should be lit, Bottom should be dark)")
    try:
        dev.set_configuration()
        dev.write(0x03, buffer, timeout=1000)
        print("Sent.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
