"""
Multi-Protocol Diagnostic for Z-10 LCD
Tests various Report IDs and offsets to find what "takes over" the screen.
"""
import usb.core
import usb.util
import usb.backend.libusb1
import os
import time

VID = 0x046D
PID = 0x0A07

def test_report(dev, report_id, data_byte, description):
    print(f"Testing {description} (Report ID: {hex(report_id)}, Data: {hex(data_byte)})...")
    buffer = bytearray([report_id] + [data_byte] * 991)
    try:
        dev.write(0x03, buffer, timeout=1000)
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    backend_path = os.path.join(os.getcwd(), "libusb-1.0.dll")
    print(f"Using libusb DLL from: {backend_path}")
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: backend_path)
    
    dev = usb.core.find(idVendor=VID, idProduct=PID, backend=backend)
    
    if dev is None:
        print("[FAIL] Device not found")
        return

    print(f"[OK] Found {dev.product}")

    try:
        dev.set_configuration()
        
        # Test 1: Report ID 0x03 (Standard G15 v1) - ALL WHITE
        test_report(dev, 0x03, 0xFF, "Standard G15 v1 (White)")
        time.sleep(2)
        
        # Test 2: Report ID 0x03 - ALL BLACK
        test_report(dev, 0x03, 0x00, "Standard G15 v1 (Black)")
        time.sleep(2)
        
        # Test 3: Report ID 0x01 (G15 v2/Other Logitech)
        test_report(dev, 0x01, 0xFF, "Report ID 0x01 (Alternative)")
        time.sleep(2)
        
        # Test 4: Report ID 0x11 (G19/Color LCDs)
        test_report(dev, 0x11, 0xFF, "Report ID 0x11 (Alternative)")
        time.sleep(2)
        
        # Test 5: Initialization attempt (Feature Reports)
        print("Testing Feature Report 0x01 (Potential Init)...")
        try:
            # Some devices need a feature report to unlock graphics mode
            dev.ctrl_transfer(0x21, 0x09, 0x0301, 0x02, [0x01, 0x81])
            print("  Feature report 0x01 sent.")
        except:
            print("  Feature report 0x01 failed (expected on some systems).")

        print("\nSearching for any pulse... (Sending 0xFF to Report 0x03 every 500ms)")
        for i in range(10):
            test_report(dev, 0x03, 0xFF, f"Pulse {i+1}")
            time.sleep(0.5)

    except Exception as e:
        print(f"[ERROR] Communication failed: {e}")
    finally:
        usb.util.dispose_resources(dev)
        print("\nTest finished.")

if __name__ == "__main__":
    main()
