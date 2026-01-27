"""
Magic Packet & Mode Switch Test for Z-10
1. Reverts to the EXACT 992-byte buffer size that worked previously.
2. Spams Feature Reports 0x01 and 0x02 to force "External Mode".
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
        
        print("Starting Magic Packet Test...")
        print("Prepare to press the 'DISPLAY' button on the speaker if nothing happens!")
        
        # 1. THE PAYLOAD (Exact 992 bytes)
        # 1 byte ID + 991 bytes Data
        # We fill it with 0xFF (White) to be obvious
        buffer = bytearray([REPORT_ID] + [0xFF] * 991)
        print(f"Buffer size: {len(buffer)} bytes")
        
        # 2. THE LOOP
        for i in range(1, 21):
            print(f"  Attempt {i}/20: Sending Mode Switch + Data...")
            
            # A. Try to force "External Mode" via Feature Reports
            try:
                # Feature 0x02 = Mode? (Value 1 = On)
                dev.ctrl_transfer(0x21, 0x09, 0x0302, 0x0002, [0x01])
            except:
                pass
                
            try:
                # Feature 0x01 = Wake? (Value 1 = On)
                dev.ctrl_transfer(0x21, 0x09, 0x0301, 0x0002, [0x01])
            except:
                pass

            # B. Send the Data (Interrupt Out)
            try:
                dev.write(0x03, buffer, timeout=1000)
            except Exception as e:
                print(f"    Write failed: {e}")
            
            time.sleep(0.5)

        print("\nTest Complete.")

    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
