"""
Surgical Test for Z-10 LCD
Tests individual pixels to determine coordinate mapping.
"""
import usb.core
import usb.util
import usb.backend.libusb1
import os
import time

VID = 0x046D
PID = 0x0A07

def send_packet(dev, data_bits):
    buffer = bytearray([0x03] + [0x00] * 991)
    # Pack bits into buffer[1:]
    for i, bit in enumerate(data_bits):
        if bit:
            byte_idx = 1 + (i // 8)
            bit_idx = i % 8
            if byte_idx < 992:
                buffer[byte_idx] |= (1 << bit_idx)
    dev.write(0x03, buffer, timeout=1000)

def main():
    backend_path = os.path.join(os.getcwd(), "libusb-1.0.dll")
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: backend_path)
    dev = usb.core.find(idVendor=VID, idProduct=PID, backend=backend)
    
    if dev is None:
        print("Device not found")
        return
        
    try:
        dev.set_configuration()
        
        # Test 1: Single Dot at (0,0)
        print("Test 1: Single dot at Top-Left (Wait 3s)")
        bits = [0] * (160 * 43)
        bits[0] = 1
        send_packet(dev, bits)
        time.sleep(3)
        
        # Test 2: First Row only
        print("Test 2: Single line at top row (Wait 3s)")
        bits = [0] * (160 * 43)
        for i in range(160):
            bits[i] = 1
        send_packet(dev, bits)
        time.sleep(3)
        
        # Test 3: First Column only
        print("Test 3: Single vertical line at left edge (Wait 3s)")
        bits = [0] * (160 * 43)
        for i in range(43):
            bits[i * 160] = 1
        send_packet(dev, bits)
        time.sleep(3)
        
        # Test 4: Checkerboard (8x8)
        print("Test 4: 8x8 Checkerboard (Wait 3s)")
        bits = [0] * (160 * 43)
        for y in range(43):
            for x in range(160):
                if ((x // 8) + (y // 8)) % 2 == 0:
                    bits[y * 160 + x] = 1
        send_packet(dev, bits)
        
    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
