"""
Read/Write Loop for Z-10
1. Spawns a thread to CONTINUOUSLY read from Endpoint 0x83 (Input/Buttons).
   - This "drains" the buffer so the firmware knows we are listening.
2. Main thread writes "Solid White" to Endpoint 0x03 (Display).
"""
import usb.core
import usb.util
import usb.backend.libusb1
import os
import time
import threading

VID = 0x046D
PID = 0x0A07
REPORT_ID = 0x03

keep_running = True

def input_reader(dev):
    """Continuously reads from the input endpoint to keep the pipe clear."""
    print("  [Thread] Input reader started (EP 0x83)...")
    while keep_running:
        try:
            # Endpoint 0x83, 64 bytes, short timeout
            dev.read(0x83, 64, timeout=100)
        except usb.core.USBError:
            pass # Timeout is normal if no buttons pressed
        except Exception as e:
            print(f"  [Thread] Error: {e}")
            break
    print("  [Thread] Input reader stopped.")

def main():
    global keep_running
    backend_path = os.path.join(os.getcwd(), "libusb-1.0.dll")
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: backend_path)
    dev = usb.core.find(idVendor=VID, idProduct=PID, backend=backend)
    
    if dev is None:
        print("Device not found")
        return

    try:
        dev.set_configuration()
        
        # Start Input Reader Thread
        thread = threading.Thread(target=input_reader, args=(dev,))
        thread.daemon = True
        thread.start()
        
        print("Starting Read/Write Loop (Check LCD!)...")
        
        # 1. Send "Wake Up" Features again, just in case
        try:
            dev.ctrl_transfer(0x21, 0x09, 0x0301, 0x0002, [0x01]) # Wake
            dev.ctrl_transfer(0x21, 0x09, 0x0302, 0x0002, [0x01]) # Mode
        except:
            pass
            
        # 2. Graphics Loop
        # 992 bytes (Report 0x03 + 991 bytes 0xFF)
        payload = bytearray([REPORT_ID] + [0xFF] * 991)
        
        for i in range(50): # Run for ~10 seconds
            try:
                dev.write(0x03, payload, timeout=1000)
                if i % 5 == 0:
                    print(f"  Sent Frame {i}")
            except Exception as e:
                print(f"  Write Error: {e}")
            
            time.sleep(0.2)
            
    except KeyboardInterrupt:
        pass
    finally:
        keep_running = False
        time.sleep(0.5) # Let thread finish
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
