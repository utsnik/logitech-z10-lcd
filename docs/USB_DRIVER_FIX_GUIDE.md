# Fixing Z-10 LCD USB Driver Access

## Problem

LCDHost and Logitech Gaming Software cannot detect the Z-10 LCD display because:

1. **Windows uses a generic USB Audio driver** for the entire Z-10 device
2. The LCD interface (HID) is **not exposed separately** to applications
3. Direct HID access is blocked by the audio driver claiming all interfaces

## Solution

We need to install a **WinUSB** or **libusb-win32** driver for the LCD interface only, using **Zadig**.

> [!IMPORTANT]
> This will NOT affect your audio! The Z-10 has multiple USB interfaces, and we'll only change the driver for the LCD interface.

---

## Understanding Z-10 USB Interfaces

The Logitech Z-10 (VID: `046D`, PID: `0A07`) exposes **multiple USB interfaces**:

| Interface | Type | Description | Current Driver |
|-----------|------|-------------|----------------|
| Interface 0 | USB Audio | Audio playback | ✅ Windows USB Audio Driver |
| Interface 1 | HID | LCD Display & Controls | ❌ Claimed by Audio Driver |
| Interface 2+ | HID | Touch controls, buttons | ❌ Claimed by Audio Driver |

**The Problem**: Windows' USB audio driver claims ALL interfaces, blocking HID access to the LCD.

**The Solution**: Use Zadig to install WinUSB driver for Interface 1 (LCD) only.

---

## Step-by-Step Fix

### Step 1: Download Zadig

1. Go to https://zadig.akeo.ie/
2. Download the latest version (Zadig 2.8 or newer)
3. Save to `c:\Users\Igland\logitech z-10\zadig.exe`

### Step 2: Run Zadig as Administrator

1. Right-click `zadig.exe` → **Run as administrator**
2. In Zadig, click **Options** → Enable **"List All Devices"**

### Step 3: Identify the LCD Interface

1. From the dropdown, look for one of these entries:
   - `Logitech Z-10` or
   - `USB Audio Device` with VID `046D` and PID `0A07` or
   - `USB Composite Device (Interface X)` where X is the LCD interface

2. **Important**: You may see multiple entries for the Z-10. Look for:
   - The one labeled as **HID** or **Interface 1**
   - NOT the "USB Audio" entry (that's for sound!)

### Step 4: Install WinUSB Driver

1. In the **target driver** dropdown (right side), select:
   - **WinUSB** (recommended) or
   - **libusb-win32**

2. Click **"Replace Driver"** or **"Install Driver"**

3. Wait for the installation to complete

4. **Important**: If you accidentally selected the wrong interface and audio stops working:
   - Go back to Zadig
   - Select the audio interface
   - Replace driver with "USB Audio Class Driver"

### Step 5: Verify Installation

Open Device Manager and check:

```powershell
# Check for WinUSB device
Get-PnpDevice | Where-Object { $_.FriendlyName -like "*Z-10*" -or $_.FriendlyName -like "*046D*" }
```

You should now see the Z-10 LCD listed separately with a WinUSB driver.

---

## Alternative: Manual USB Interface Detection

If Zadig doesn't clearly show which interface is the LCD, use this script:

```powershell
# List all Z-10 USB interfaces
$usbDevices = Get-PnpDevice | Where-Object { $_.InstanceId -like "*VID_046D&PID_0A07*" }

foreach ($device in $usbDevices) {
    Write-Host "`nDevice: $($device.FriendlyName)" -ForegroundColor Cyan
    Write-Host "Instance ID: $($device.InstanceId)" -ForegroundColor Gray
    Write-Host "Status: $($device.Status)" -ForegroundColor $(if($device.Status -eq "OK"){"Green"}else{"Red"})
    
    # Try to get interface number
    if ($device.InstanceId -match "MI_(\d+)") {
        Write-Host "Interface: $($matches[1])" -ForegroundColor Yellow
    }
}
```

---

## What This Changes

### Before:
```
Z-10 USB Device (046D:0A07)
├── Interface 0: Audio (USB Audio Driver) ✅
├── Interface 1: LCD (USB Audio Driver) ❌ BLOCKED
└── Interface 2: Controls (USB Audio Driver) ❌ BLOCKED
```

### After:
```
Z-10 USB Device (046D:0A07)
├── Interface 0: Audio (USB Audio Driver) ✅
├── Interface 1: LCD (WinUSB) ✅ ACCESSIBLE!
└── Interface 2: Controls (USB Audio Driver) ❌ BLOCKED
```

---

## Testing After Driver Installation

Once the driver is installed, we can test USB communication:

### Option 1: Test with LCDHost
1. Run LCDHost
2. Go to Settings → Devices
3. Check if Z-10 LCD is now detected

### Option 2: Test with Python
```python
import hid

# List all HID devices
for device in hid.enumerate():
    if device['vendor_id'] == 0x046D and device['product_id'] == 0x0A07:
        print(f"Found Z-10 Interface: {device['interface_number']}")
        print(f"  Path: {device['path']}")
        print(f"  Usage: {device['usage']}")
```

---

## Troubleshooting

### Audio Stopped Working
- You installed the driver on the wrong interface (Interface 0)
- **Fix**: Use Zadig to restore "USB Audio Class Driver" on Interface 0

### Still Can't See LCD
- The LCD might be on a different interface (try Interface 2 or 3)
- **Fix**: Try installing WinUSB on each interface one by one

### Multiple Interface Numbers
- The Z-10 may present differently on your system
- **Fix**: Check Device Manager for all Z-10 subdevices and note their interface numbers

---

## Next Steps

After successful driver installation:

1. ✅ Test with LCDHost again
2. ✅ Test with Python HID library
3. ✅ Begin protocol reverse engineering
4. ✅ Build our custom LCD application

