"""
Z-10 Button Sniffer
-------------------
Reads from Endpoint 0x83 (Input) and prints any data received.
Use this to find out what "Button 1", "Button 2", etc. send.
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
        # We assume the device is already configured/claimed by previous scripts or logic.
        # If not, we might need to set config, but let's try not to reset the LCD if possible.
        if dev.get_active_configuration() is None:
            dev.set_configuration()
        
        try:
             usb.util.claim_interface(dev, 2)
        except:
             pass

        print("Button Sniffer Started.")
        print("Press the LCD buttons (1, 2, 3, 4)...")
        print("Press Ctrl+C to stop.")

        while True:
            try:
                # Read 64 bytes from Endpoint 0x83
                data = dev.read(0x83, 64, timeout=100)
                
                # If we get data, print it!
                if data:
                    print(f"Data: {list(data)}")
                    # Hex format for easier reading
                    hex_str = ' '.join(f'{x:02X}' for x in data)
                    print(f"Hex:  {hex_str}")
                    print("-" * 20)
                    
            except usb.core.USBError as e:
                # Timeout is normal
                pass
            except Exception as e:
                print(f"Error: {e}")
                break
                
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass
    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
