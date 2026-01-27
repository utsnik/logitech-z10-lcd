"""
Golden Sample - Continuous White Screen
Sends the standard G15 packet (Report 0x03 + 991 bytes 0xFF) continuously.
This mimics the state where you saw "glitches" (which means it matches the protocol!).
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
        print("Sending Continuous White Screen...")
        print("Keep watching the LCD as you plug it in/out if needed.")
        print("Press Ctrl+C to stop.")

        # 992 bytes total (1 ID + 991 Data)
        payload = bytearray([REPORT_ID] + [0xFF] * 991)
        
        while True:
            try:
                dev.write(0x03, payload, timeout=1000)
                time.sleep(0.1)  # 10 FPS
            except usb.core.USBError as e:
                # If device is unplugged/replugged, this will catch it
                print(f"Waiting for device... ({e})")
                time.sleep(1)
                # Try to reconnect
                dev = usb.core.find(idVendor=VID, idProduct=PID, backend=backend)
                if dev:
                    try:
                       dev.set_configuration()
                    except:
                       pass
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
