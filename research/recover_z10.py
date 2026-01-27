"""
Brute Force Recovery for Z-10 LCD
Attempts multiple offsets and payloads to re-trigger the graphics mode.
"""
import usb.core
import usb.util
import usb.backend.libusb1
import os
import time

VID = 0x046D
PID = 0x0A07

def main():
    backend_path = os.path.join(os.getcwd(), "libusb-1.0.dll")
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: backend_path)
    dev = usb.core.find(idVendor=VID, idProduct=PID, backend=backend)
    
    if dev is None:
        print("Device not found")
        return

    try:
        dev.set_configuration()
        
        # Strategy 1: The "Everything On" Heavy Reset
        # Sometimes the Z-10 needs a full buffer to override the internal logo.
        print("Strategy 1: Full 991-byte 0xFF burst...")
        for _ in range(3):
            buffer = bytearray([0x03] + [0xFF] * 991)
            dev.write(0x03, buffer, timeout=1000)
            time.sleep(0.5)

        # Strategy 2: Feature Report Init (G15 style)
        print("Strategy 2: Trying Feature Report initialization...")
        try:
            # bmRequestType: 0x21 (Host to Device, Class, Interface)
            # bRequest: 0x09 (SET_REPORT)
            # wValue: 0x0301 (Type: Feature, ID: 01)
            # wIndex: 0x0002 (Interface 2)
            dev.ctrl_transfer(0x21, 0x09, 0x0301, 0x0002, [0x01, 0x81])
            print("  Feature Report (Init) sent")
        except:
            pass

        # Strategy 3: Offsets (Sliding window of 860 bytes)
        print("Strategy 3: Sliding 860-byte window (This may take 15s)...")
        # 991 total bytes. Visible area is 860 bytes.
        # Let's try every 10 byte offset.
        for offset in range(0, 132, 10):
            print(f"  Testing offset {offset}...")
            buffer = bytearray([0x03] + [0x00] * 991)
            # Fill the 860-byte "image" area with noise
            for i in range(860):
                if 1 + offset + i < 992:
                    buffer[1 + offset + i] = 0xAA # Pattern
            dev.write(0x03, buffer, timeout=1000)
            time.sleep(0.8)

    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
