import mmap
import ctypes
import time

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

class RTSS_APP_ENTRY_V2(ctypes.Structure):
    _fields_ = [
        ("dwProcessId", ctypes.c_uint32),
        ("szName", ctypes.c_char * 260),
        ("dwFlags", ctypes.c_uint32),
        ("dwTime0", ctypes.c_uint32),
        ("dwTime1", ctypes.c_uint32),
        ("dwFrames", ctypes.c_uint32),
        ("dwFrameTime", ctypes.c_uint32),
        ("dwStatFlags", ctypes.c_uint32)
    ]

try:
    print("Mapping 4KB header...")
    tmp = mmap.mmap(0, 4096, "RTSSSharedMemoryV2")
    header = RTSS_SHARED_MEMORY_V2.from_buffer_copy(tmp.read(ctypes.sizeof(RTSS_SHARED_MEMORY_V2)))
    
    app_end = header.dwAppArrOffset + (header.dwAppArrSize * header.dwAppEntrySize)
    osd_end = header.dwOSDArrOffset + (header.dwOSDArrSize * header.dwOSDEntrySize)
    total_size = max(app_end, osd_end)
    if total_size < 1024: total_size = 65536
    
    tmp.close()
    
    print(f"Mapping Full Size: {total_size}")
    m = mmap.mmap(0, total_size, "RTSSSharedMemoryV2")
    
    print(f"\n--- RTSS App Entries ({header.dwAppArrSize} slots) ---")
    
    count = 0
    for i in range(header.dwAppArrSize):
        offset = header.dwAppArrOffset + (i * header.dwAppEntrySize)
        m.seek(offset)
        buf = m.read(ctypes.sizeof(RTSS_APP_ENTRY_V2))
        app = RTSS_APP_ENTRY_V2.from_buffer_copy(buf)
        
        if app.dwProcessId != 0:
            name = app.szName.decode('utf-8', errors='ignore').split(chr(0))[0]
            if not name: continue
            
            # Check recency
            # RTSS timestamps are usually simple ticks? Or OS uptime?
            # dwTime1 seems to be the last update time.
            
            print(f"[{i}] PID: {app.dwProcessId} | Name: {name}")
            print(f"    Flags: {app.dwFlags:x}")
            print(f"    Frames: {app.dwFrames}")
            print(f"    FrameTime: {app.dwFrameTime} us (FPS: {1000000/max(1, app.dwFrameTime):.1f})")
            print(f"    Time1: {app.dwTime1}")
            count += 1

    print(f"\nFound {count} active processes.")
    m.close()

except Exception as e:
    print(f"Error: {e}")
