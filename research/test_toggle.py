"""
Toggle Test for Z-10 LCD
Alternates between Solid Black and Solid White every second
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
        print("Starting Toggle Test (Ctrl+C to stop)")
        print("Alternating Black/White every 1 second...")
        
        while True:
            # 1. Send Solid WHITE (All Pixels ON)
            white_buffer = bytearray([REPORT_ID] + [0xFF] * 991)
            dev.write(0x03, white_buffer, timeout=1000)
            print("  [WHITE]")
            time.sleep(1)
            
            # 2. Send Solid BLACK (All Pixels OFF)
            black_buffer = bytearray([REPORT_ID] + [0x00] * 991)
            dev.write(0x03, black_buffer, timeout=1000)
            print("  [BLACK]")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Stopped.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
