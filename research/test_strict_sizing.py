"""
STRICT SIZING TEST for Z-10 LCD
Sends exactly 991 bytes (Report 0x03 + 990 bytes data).
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
        
        # G15 v1 protocol: 1 Report ID + 990 bytes data = 991 bytes
        print("Testing STRICT 991-byte packet...")
        buffer = bytearray([REPORT_ID] + [0xFF] * 990)
        
        # Write to Endpoint 0x03
        try:
            dev.write(0x03, buffer, timeout=1000)
            print("Sent 991 bytes [0xFF]. Check LCD!")
        except Exception as e:
            print(f"Error: {e}")

    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
