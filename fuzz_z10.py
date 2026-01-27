"""
Z-10 Protocol Fuzzer
WARNING: This script sends various packet sizes and IDs to the LCD.
It attempts to find the "unlock" combination.
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
        print("Starting Fuzzer...")
        
        # Test 1: Report ID 0x03 with varying sizes
        # Standard G15 is ~992. Z-10 might be 860 (exact pixels) or something else.
        print("\n--- Testing Report 0x03 Sizes ---")
        for size in range(850, 1000, 2):  # Try even sizes e.g. 850, 852...
            try:
                # payload: ID + [FF]...
                payload = bytearray([0x03] + [0xFF] * (size - 1))
                dev.write(0x03, payload, timeout=100) # Fast timeout
                print(f"Size {size}: SENT")
            except:
                pass # Expected error for wrong sizes
            
            if size % 50 == 0:
                print(f"  ...at {size}")
        
        # Test 2: Other Report IDs (0x01, 0x02, 0x04)
        print("\n--- Testing Other Report IDs ---")
        for report_id in [0x01, 0x02, 0x04]:
            payload = bytearray([report_id] + [0xFF] * 63) # Small packet
            try:
                dev.write(0x03, payload, timeout=100)
                print(f"Report {hex(report_id)} (64b): SENT")
            except:
                pass
                
        # Test 3: Feature Report Unlock attempts
        print("\n--- Testing Feature Unlocks ---")
        for req_val in [0x0300, 0x0301, 0x0302]: # Feature Request types
            try:
                dev.ctrl_transfer(0x21, 0x09, req_val, 0x0002, [0x01])
                print(f"Feature {hex(req_val)}: SENT")
            except:
                pass

        print("\nFuzzing complete. Did you see ANY flicker?")

    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
