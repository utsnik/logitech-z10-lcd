import mmap
import ctypes
import struct

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
    m = mmap.mmap(0, 65536, "RTSSSharedMemoryV2")
    m.seek(0)
    buf = m.read(ctypes.sizeof(RTSS_SHARED_MEMORY_V2))
    header = RTSS_SHARED_MEMORY_V2.from_buffer_copy(buf)
    print(f"Signature Found: {header.dwSignature} (Hex: {header.dwSignature:x})")
    print(f"Expected: {0x53535452} (Hex: 53535452)")
    print(f"Version: {header.dwVersion}")
    m.close()
except Exception as e:
    print(f"Error: {e}")
