"""
Initialization and Backlight Test for Z-10 LCD
Tests if the device needs a specific 'mode' or 'backlight' command to show graphics.
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
        
        # Test A: Set Brightness/Backlight (Report 0x02)
        # Often 0x02 [brightness_level] [0x00...]
        print("Sending Backlight ON command (Report 0x02)...")
        bl_buffer = bytearray([0x02] + [0xFF] * 63) # Most 0x02 reports are 64 bytes
        try:
            dev.write(0x03, bl_buffer, timeout=1000) # Interface 2 usually has index 0x03 for writes
        except:
            pass
            
        # Test B: Initialization Sequence
        # Some devices need 0x01 [0x81/0x82] to start
        print("Sending Init Sequence (Report 0x01)...")
        init_buffer = bytearray([0x01, 0x81, 0x00, 0x00, 0x00])
        try:
            dev.write(0x03, init_buffer, timeout=1000)
        except:
            pass

        time.sleep(1)

        # Test C: Full White (Report 0x03)
        print("Sending FULL WHITE (Report 0x03)...")
        fill_buffer = bytearray([0x03] + [0xFF] * 991)
        dev.write(0x03, fill_buffer, timeout=1000)
        
        print("Done. Is the screen white now?")

    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
