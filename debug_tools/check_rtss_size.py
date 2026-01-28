import mmap
import ctypes

class RTSS_SHARED_MEMORY_V2(ctypes.Structure):
    _fields_ = [
        ("dwSignature", ctypes.c_uint32),
        ("dwVersion", ctypes.c_uint32),
        ("dwAppEntrySize", ctypes.c_uint32),
        ("dwAppArrOffset", ctypes.c_uint32),
        ("dwAppArrSize", ctypes.c_uint32),
        ("dwOSDEntrySize", ctypes.c_uint32),
        ("dwOSDArrOffset", ctypes.c_uint32),
        ("dwOSDArrSize", ctypes.c_uint32),
        ("dwOSDFrame", ctypes.c_uint32)
    ]

try:
    # Map enough for header
    m = mmap.mmap(0, 4096, "RTSSSharedMemoryV2")
    buf = m.read(ctypes.sizeof(RTSS_SHARED_MEMORY_V2))
    header = RTSS_SHARED_MEMORY_V2.from_buffer_copy(buf)
    
    print(f"Sig: {header.dwSignature:x}")
    print(f"AppOffset: {header.dwAppArrOffset}")
    print(f"AppCount: {header.dwAppArrSize}")
    print(f"AppSize: {header.dwAppEntrySize}")
    print(f"OSDOffset: {header.dwOSDArrOffset}")
    print(f"OSDCount: {header.dwOSDArrSize}")
    print(f"OSDSize: {header.dwOSDEntrySize}")
    
    # Calculate end of App array
    app_end = header.dwAppArrOffset + (header.dwAppArrSize * header.dwAppEntrySize)
    print(f"AppEnd: {app_end}")
    
    # Calculate end of OSD array
    osd_end = header.dwOSDArrOffset + (header.dwOSDArrSize * header.dwOSDEntrySize)
    print(f"OSDEnd: {osd_end}")
    
    m.close()
except Exception as e:
    print(f"Error: {e}")
