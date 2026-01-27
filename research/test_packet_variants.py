"""
Packet Variants Test for Z-10 LCD
Tests Control Transfers, Chunking, and Padding to bypass the "Logo Lock".
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
        
        # Payload: Report ID + Solid White Data
        # Base size = 992 bytes (Protocol G15 v1 standard-ish)
        payload = bytearray([REPORT_ID] + [0xFF] * 991)
        
        # Method 1: Control Transfer (SET_REPORT)
        # This bypasses the Endpoint 0x03 and asks the main chip to accept data directly
        print("Test 1: Control Transfer SET_REPORT (Wait 3s)...")
        try:
            # bmRequestType: 0x21 (Host->Device, Class, Interface)
            # bRequest: 0x09 (SET_REPORT)
            # wValue: 0x0203 (ReportType: Output(02), ReportID: 03)
            # wIndex: 0x0002 (Interface 2)
            dev.ctrl_transfer(0x21, 0x09, 0x0203, 0x0002, payload)
            print("  Sent via Control Transfer.")
        except Exception as e:
            print(f"  Control Transfer failed: {e}")
            
        time.sleep(3)
        
        # Method 2: Manual Chunking (64 bytes)
        # Maybe the device can't handle a huge burst and needs small bites
        print("Test 2: Manual 64-byte Chunks to EP 0x03 (Wait 3s)...")
        try:
            # We just write the whole thing, but maybe we can simulate "slow" writing?
            # Actually, standard write() handles splitting, but let's try a slightly different size
            # that is a multiple of 64.
            padded_payload = payload + bytearray([0x00] * (1024 - len(payload))) # Pad to 1024
            dev.write(0x03, padded_payload, timeout=1000)
            print("  Sent 1024 bytes (Padding to 64-byte alignment).")
        except Exception as e:
            print(f"  Padding write failed: {e}")

        time.sleep(3)
        
        # Method 3: "Tickle" + Write
        # Send a tiny packet first to wake it up?
        print("Test 3: 'Tickle' 0x01 then Write...")
        try:
            dev.ctrl_transfer(0x21, 0x09, 0x0301, 0x0002, [0x01]) # Feature report 1
            time.sleep(0.1)
            dev.write(0x03, payload, timeout=1000)
            print("  Sent Tickle + Payload.")
        except Exception as e:
            print(f"  Tickle failed: {e}")

    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
