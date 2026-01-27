"""
Interactive Z-10 Tuner
----------------------
Controls:
 [1] Toggle Data (White/Black/Stripes)
 [2] Toggle Inversion (0xFF vs 0x00)
 [Q]/[A] Adjust Feature 0x01 Value (Contrast?)
 [W]/[S] Adjust Feature 0x02 Value (Brightness?)
 [E]/[D] Adjust Feature 0x03 Value (Mode?)
 [R]/[F] Adjust Feature 0x04 Value (Unknown?)
 [T] Send Tickle (0x01 command)
 
 [X] Exit
"""
import usb.core
import usb.util
import usb.backend.libusb1
import os
import time
import msvcrt # For key presses on Windows

VID = 0x046D
PID = 0x0A07
REPORT_ID = 0x03

# State
data_pattern = 0 # 0=White, 1=Black, 2=Stripes
inverted = False
feat_vals = {1: 0x00, 2: 0x01, 3: 0x00, 4: 0x00} # Default guess

def send_feature(dev, feat_id, val):
    try:
        # 0x0300 | feat_id
        wValue = (0x03 << 8) | feat_id
        dev.ctrl_transfer(0x21, 0x09, wValue, 0x0002, [val])
        print(f"  Feature {hex(feat_id)} -> {hex(val)}   ", end='\r')
    except Exception as e:
        print(f"  Err Feat {hex(feat_id)}: {e}   ", end='\r')

def send_display(dev):
    global data_pattern, inverted
    
    buffer = bytearray(992)
    buffer[0] = REPORT_ID
    
    # Fill data
    fill_val = 0xFF if not inverted else 0x00
    if data_pattern == 1: # Black
        fill_val = 0x00 if not inverted else 0xFF
    
    for i in range(1, 992):
        if data_pattern == 2: # Stripes
            # 0xAA = 10101010
            buffer[i] = 0xAA if not inverted else 0x55
        else:
            buffer[i] = fill_val

    try:
        dev.write(0x03, buffer, timeout=100)
    except:
        pass

def main():
    global data_pattern, inverted
    
    backend_path = os.path.join(os.getcwd(), "libusb-1.0.dll")
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: backend_path)
    dev = usb.core.find(idVendor=VID, idProduct=PID, backend=backend)
    
    if dev is None:
        print("Device not found")
        return

    try:
        dev.set_configuration()
        print("Interactive Tuner Started.")
        print("Press keys to adjust. LCD is refreshing...")
        
        while True:
            # Check for key press
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                
                if key == 'x': break
                elif key == '1': 
                    data_pattern = (data_pattern + 1) % 3
                    print(f"\nPattern: {['White','Black','Stripes'][data_pattern]}")
                elif key == '2': 
                    inverted = not inverted
                    print(f"\nInverted: {inverted}")
                elif key == 't':
                     send_feature(dev, 0x01, 0x81) # Try "Wake"
                     print("\nSent Tickle")
                
                # Feature Adjustments
                elif key == 'q': feat_vals[1] = (feat_vals[1] + 1) % 256; send_feature(dev, 1, feat_vals[1])
                elif key == 'a': feat_vals[1] = (feat_vals[1] - 1) % 256; send_feature(dev, 1, feat_vals[1])
                elif key == 'w': feat_vals[2] = (feat_vals[2] + 1) % 256; send_feature(dev, 2, feat_vals[2])
                elif key == 's': feat_vals[2] = (feat_vals[2] - 1) % 256; send_feature(dev, 2, feat_vals[2])
                elif key == 'e': feat_vals[3] = (feat_vals[3] + 1) % 256; send_feature(dev, 3, feat_vals[3])
                elif key == 'd': feat_vals[3] = (feat_vals[3] - 1) % 256; send_feature(dev, 3, feat_vals[3])
                elif key == 'r': feat_vals[4] = (feat_vals[4] + 1) % 256; send_feature(dev, 4, feat_vals[4])
                elif key == 'f': feat_vals[4] = (feat_vals[4] - 1) % 256; send_feature(dev, 4, feat_vals[4])

            # Continuous Refresh
            send_display(dev)
            time.sleep(0.05)

    finally:
        usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
