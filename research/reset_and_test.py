"""
USB Reset and Fill Test for Z-10 LCD
Attempts to reset the USB device and then send a 'Fill' command.
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
        print("[FAIL] Z-10 not found!")
        return

    print(f"[OK] Found Z-10. Attempting USB reset...")
    
    try:
        # 1. Reset the device
        dev.reset()
        print("[OK] Device reset command sent. Waiting 2s for re-enumeration...")
        time.sleep(2)
        
        # 2. Re-find the device after reset
        dev = usb.core.find(idVendor=VID, idProduct=PID, backend=backend)
        if dev is None:
            print("[FAIL] Device did not come back after reset!")
            return
            
        dev.set_configuration()
        print("[OK] Re-connected. Sending FILL command (0xFF)...")
        
        # 3. Send Fill Screen (0xFF)
        buffer = bytearray([REPORT_ID] + [0xFF] * 991)
        bytes_written = dev.write(0x03, buffer, timeout=1000)
        print(f"[OK] Sent {bytes_written} bytes.")
        
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        usb.util.dispose_resources(dev)

    print("\nCheck the LCD! Did it turn White?")

if __name__ == "__main__":
    main()
