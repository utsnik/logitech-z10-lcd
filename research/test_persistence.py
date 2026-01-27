"""
Persistence Test for Z-10 LCD
1. Tries to ENABLE graphics mode via Feature Report 0x02 (common on Logitech).
2. Sends the image REPEATEDLY (20 times/sec) to override the default "Logo/Volume" screen.
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
        
        # --- ATTEMPT 1: MODE SWITCH (Feature 0x02) ---
        print("Attempting to lock 'Graphics Mode' (Feature 0x02)...")
        try:
            # Try sending a "Set Mode" feature report
            # 0x02 is often "Mode"
            # Data [0x01] = On?
            dev.ctrl_transfer(0x21, 0x09, 0x0302, 0x0002, [0x01])
            print("  Sent Feature 0x02 [0x01]")
        except:
            pass
            
        # --- ATTEMPT 2: PERSISTENCE LOOP ---
        print("\nStarting High-Speed Refresh (Press Ctrl+C to stop)...")
        print("Sending Solid White @ 20Hz. Watch for flickering!")
        
        payload = bytearray([REPORT_ID] + [0xFF] * 991)
        
        count = 0
        t_start = time.time()
        
        while True:
            try:
                dev.write(0x03, payload, timeout=100)
                count += 1
                if count % 20 == 0:
                    print(f"  Sent {count} frames...", end='\r')
                
                # Sleep a tiny bit (20 fps = 0.05s)
                time.sleep(0.05)
                
                # Stop after 10 seconds of success so we don't spam forever
                if time.time() - t_start > 10:
                    break
                    
            except usb.core.USBError as e:
                print(f"\n  Write error: {e}")
                time.sleep(0.5)
                
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        usb.util.dispose_resources(dev)

    print("\n\nDid the screen turn white (or at least flicker) during the spam?")

if __name__ == "__main__":
    main()
