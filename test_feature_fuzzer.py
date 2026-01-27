"""
Feature Report Fuzzer for Z-10
Tries to brute-force "Unlock" / "Mode Switch" commands.
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
        print("Starting Feature Report Fuzzer...")
        print("Watch the LCD for ANY flicker!")

        # Standard Data Packet (White Screen)
        # We send this after every feature attempt to see if it "worked"
        white_screen = bytearray([0x03] + [0xFF] * 991)

        # Fuzz Feature Reports IDs 0x00 to 0x0F
        for report_id in range(0, 5): # 0, 1, 2, 3, 4
            print(f"\nTesting Feature Report ID: {hex(report_id)}")
            
            # Fuzz Values 0x00 to 0x0F
            for val in range(0, 5): # 0, 1, 2, 3, 4
                try:
                    # bmRequestType: 0x21 (Host->Device, Class, Interface)
                    # bRequest: 0x09 (SET_REPORT)
                    # wValue: (0x03 << 8) | report_id  (Feature Report)
                    # wIndex: 0x0002 (Interface 2)
                    wValue = (0x03 << 8) | report_id
                    
                    # Try sending 1 byte payload
                    dev.ctrl_transfer(0x21, 0x09, wValue, 0x0002, [val])
                    print(f"  Sent Feature {hex(report_id)} = {hex(val)}")
                    
                    # Immediately try to write to display
                    dev.write(0x03, white_screen, timeout=50) # Fast timeout
                    
                except Exception:
                    pass
                
                time.sleep(0.05)

    finally:
        usb.util.dispose_resources(dev)

    print("\nFuzzing complete. Did anything happen?")

if __name__ == "__main__":
    main()
