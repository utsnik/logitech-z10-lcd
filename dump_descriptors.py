"""
Z-10 Descriptor Dump
Dumps all configurations, interfaces, and endpoints.
"""
import usb.core
import usb.util
import usb.backend.libusb1
import os

VID = 0x046D
PID = 0x0A07

def main():
    backend_path = os.path.join(os.getcwd(), "libusb-1.0.dll")
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: backend_path)
    dev = usb.core.find(idVendor=VID, idProduct=PID, backend=backend)
    
    if dev is None:
        print("Device not found")
        return

    print(f"Device: {dev.product}")
    print(f"Vendor ID: {hex(dev.idVendor)}")
    print(f"Product ID: {hex(dev.idProduct)}")
    
    for config in dev:
        print(f"\nConfiguration {config.bConfigurationValue}:")
        for interface in config:
            print(f"  Interface {interface.bInterfaceNumber}, Alt {interface.bAlternateSetting}:")
            for endpoint in interface:
                print(f"    Endpoint {hex(endpoint.bEndpointAddress)}:")
                print(f"      Type: {usb.util.endpoint_type(endpoint.bmAttributes)}")
                print(f"      Direction: {'IN' if usb.util.endpoint_direction(endpoint.bEndpointAddress) == usb.util.ENDPOINT_IN else 'OUT'}")
                print(f"      Max Packet Size: {endpoint.wMaxPacketSize}")

    usb.util.dispose_resources(dev)

if __name__ == "__main__":
    main()
