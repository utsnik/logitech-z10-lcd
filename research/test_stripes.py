"""
Stripe Pattern for Z-10 LCD
Sends 20 bytes (1 row) ON, then 20 bytes OFF.
If the LCD is 160px wide, this should show clean horizontal stripes.
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
    
    # Fill with stripes
    # Row stride = 160 / 8 = 20 bytes
    for row in range(43):
        if row % 2 == 0:
            start = 1 + (row * 20)
            for i in range(20):
                if start + i < 992:
                    buffer[start + i] = 0xFF
                    
    print("Sending Horizontal Stripe Pattern (Expected: Alternating black/white lines)")
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
