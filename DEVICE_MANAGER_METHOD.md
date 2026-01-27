# Alternative Method: Install WinUSB Driver via Device Manager

## Problem
Zadig can't see the Z-10 devices because they have Status "Unknown" in Windows. This happens when devices aren't fully initialized.

## Solution: Use Device Manager Instead

### Step 1: Open Device Manager
```powershell
devmgmt.msc
```

### Step 2: Find the Z-10 LCD Interface

In Device Manager, look for one of these sections:
- **Sound, video and game controllers**
- **Universal Serial Bus devices**
- **Other devices** (if drivers failed)

Expand and find:
- **"Z-10 USB Speaker (Interface 2)"** 
- OR **"HID-kompatibel leveranderdefinert enhet"** with properties showing VID_046D&PID_0A07&MI_02

### Step 3: Update Driver Manually

1. **Right-click** on "Z-10 USB Speaker (Interface 2)"
2. Select **"Update driver"**
3. Choose **"Browse my computer for drivers"**
4. Choose **"Let me pick from a list of available drivers on my computer"**
5. Check the box: **☑ "Show compatible hardware"**
6. In the list, look for **"WinUsb Device"** (under Microsoft or Universal)
7. Select it and click **Next**
8. Confirm the installation

### Step 4: If WinUsb Device Is Not Listed

If you don't see "WinUsb Device", we'll need to create a custom INF file:

#### 4a. Create z10_lcd.inf

Save this as `c:\Users\Igland\logitech z-10\z10_lcd.inf`:

```ini
[Version]
Signature   = "$Windows NT$"
Class       = USBDevice
ClassGUID   = {88BAE032-5A81-49f0-BC3D-A4FF138216D6}
Provider    = %ManufacturerName%
CatalogFile = z10_lcd.cat
DriverVer   = 01/27/2026,1.0.0.0

[Manufacturer]
%ManufacturerName% = Standard,NTamd64

[Standard.NTamd64]
%DeviceName% = USB_Install, USB\VID_046D&PID_0A07&MI_02

[USB_Install]
Include = winusb.inf
Needs   = WINUSB.NT

[USB_Install.Services]
Include = winusb.inf
Needs   = WINUSB.NT.Services

[USB_Install.HW]
AddReg = Dev_AddReg

[Dev_AddReg]
HKR,,DeviceInterfaceGUIDs,0x00010000,"{45C2B13C-0A1A-4DD0-9D4E-27804CE24ACE}"

[Strings]
ManufacturerName = "Logitech"
DeviceName       = "Z-10 USB Speaker LCD (Interface 2)"
```

#### 4b. Install Using Custom INF

1. In Device Manager, right-click "Z-10 USB Speaker (Interface 2)"
2. **Update driver** → **Browse my computer**
3. Click **"Have Disk..."**
4. Browse to: `c:\Users\Igland\logitech z-10\z10_lcd.inf`
5. Click **OK** and **Next**
6. Accept any unsigned driver warnings

---

## Alternative: Reset the USB Device First

Before trying the INF file, try resetting the device:

```powershell
# Uninstall the Z-10 Interface 2 device
$device = Get-PnpDevice | Where-Object { $_.FriendlyName -eq "Z-10 USB Speaker (Interface 2)" } | Select-Object -First 1
if ($device) {
    pnputil /remove-device $device.InstanceId
}

# Then unplug and replug the Z-10 speakers
# Wait for Windows to reinstall drivers
# Then try Zadig again
```

---

## Why This Happens

Windows' USB Composite driver (USBCCGP) is managing the Z-10, but it's not enumerating Interface 2 properly, leaving it in "Unknown" state. This prevents Zadig from accessing it.

By manually specifying the driver via Device Manager, we bypass Zadig and directly tell Windows to use WinUSB for that interface.
