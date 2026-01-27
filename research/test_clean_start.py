"""
Final Clean Start for Z-10
Run this AFTER fully power-cycling the speakers (Wall Plug).
1. Resets USB config.
2. Sends minimal "Wake" command.
3. Sends standard G15 v1 image.
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
        # 1. Force Clean Configuration
        dev.set_configuration()
        print("USB Configuration Set.")
        
        # 2. Clear any pending state
        try:
            dev.ctrl_transfer(0x21, 0x0A, 0x00, 0x0002, []) # SET_IDLE
        except:
            pass

        # 3. Mode Switch (Standard G15 Magic)
        print("Sending Wake/Mode commands...")
        try:
            dev.ctrl_transfer(0x21, 0x09, 0x0302, 0x0002, [0x01]) # Mode On
        except:
            pass
            
        time.sleep(0.5)

        # 4. Send Image (992 bytes)
        print("Sending White Screen...")
        payload = bytearray([REPORT_ID] + [0xFF] * 991)
        dev.write(0x03, payload, timeout=1000)
        print("Done.")

    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
