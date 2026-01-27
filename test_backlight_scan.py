"""
Backlight & Offset Scanner for Z-10
1. Cycles through potential Brightness/Contrast commands.
2. Scans a "White Bar" across the memory to find the visible area.
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
        
        print("Step 1: Testing Backlight/Contrast Modes...")
        # Try Feature Reports 0x01..0x04 with values 0, 1, 2, 100, 255
        for feat_id in [0x01, 0x02, 0x03, 0x04]:
            for val in [0x01, 0x02, 0x10, 0xFF]:
                try:
                    # Set Feature
                    dev.ctrl_transfer(0x21, 0x09, (0x03 << 8) | feat_id, 0x0002, [val])
                    print(f"  Sent Feature {hex(feat_id)} = {hex(val)}")
                    
                    # Send White Screen immediately after
                    dev.write(0x03, bytearray([0x03] + [0xFF] * 991), timeout=100)
                    time.sleep(0.5)
                except:
                    pass

        print("\nStep 2: Sliding White Window...")
        # Start with all BLACK
        base = bytearray([0x03] + [0x00] * 991)
        
        for offset in range(0, 950, 20):
            print(f"  Offset {offset}...", end='\r')
            buf = bytearray(base)
            # Make a 50-byte WHITE block
            for i in range(50):
                if 1 + offset + i < 992:
                    buf[1 + offset + i] = 0xFF
            
            try:
                dev.write(0x03, buf, timeout=100)
            except:
                pass
            time.sleep(0.1)

    finally:
        usb.util.dispose_resources(dev)

    print("\nDone.")

if __name__ == "__main__":
    main()
