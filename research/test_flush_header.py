"""
Flush & Header Test for Z-10
1. Flushes the INPUT endpoint (0x83) to clear any stuck button/events.
2. Sends G15 'Wake Up' command.
3. Tests both "No Padding" and "32-byte Padding" headers.
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
        
        # --- STEP 1: READ FLUSH (Endpoint 0x83) ---
        print("Step 1: Flushing Input Endpoint 0x83...")
        try:
            # Try to read 64 bytes, 10 times, to clear any buffers
            for i in range(10):
                data = dev.read(0x83, 64, timeout=100)
                print(f"  Read {len(data)} bytes: {list(data)}")
        except usb.core.USBError:
            print("  Input buffer empty (good).")

        time.sleep(1)

        # --- STEP 2: WAKE UP (Feature Report 0x01) ---
        print("\nStep 2: Sending Feature Report 0x01 (Wake Up)...")
        try:
            # 0x0301 = Set Feature Report ID 0x01
            dev.ctrl_transfer(0x21, 0x09, 0x0301, 0x0002, [0x01]) # Value 1 = Enable?
            print("  Wake command sent.")
        except Exception as e:
            print(f"  Wake command failed: {e}")

        time.sleep(1)

        # --- STEP 3: DATA TEST (Standard) ---
        print("\nStep 3: Standard 992-byte Write (Report 0x03 + Data)...")
        try:
            payload = bytearray([0x03] + [0xFF] * 991)
            dev.write(0x03, payload, timeout=1000)
            print("  Standard Write Sent.")
        except Exception as e:
            print(f"  Standard Write failed: {e}")

        time.sleep(2)
        
        # --- STEP 4: DATA TEST (With 32-byte Padding) ---
        # Some G15 headers are 0x03 + 32 bytes of 0x00 + Data
        print("\nStep 4: Padded Write (Report 0x03 + 31 zeros + Data)...")
        try:
            # Header: 1 byte ID + 31 bytes padding = 32 bytes total? or 33? 
            # Let's try 0x03 + 31 zeros
            header = [0x03] + [0x00] * 31
            # Remaining payload to fill 992 bytes (or just send full image)
            # 992 - 32 = 960 bytes of data space
            data = [0xFF] * 960
            payload = bytearray(header + data)
            dev.write(0x03, payload, timeout=1000)
            print("  Padded Write Sent.")
        except Exception as e:
            print(f"  Padded Write failed: {e}")

    finally:
        usb.util.dispose_resources(dev)

    print("\nCheck LCD. Any white screen?")

if __name__ == "__main__":
    main()
