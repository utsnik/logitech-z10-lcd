# SIMPLE STEP-BY-STEP: Install WinUSB in Device Manager

## The Situation
Your Z-10 Interface 2 (LCD) shows "Unknown" status. We need to manually tell Windows to use WinUSB for it.

---

## Follow These Exact Steps:

### 1. Open Device Manager
   - Press `Win + X`
   - Click **"Device Manager"**

### 2. Show Hidden Devices
   - In Device Manager: Click **View** menu → ✅ **"Show hidden devices"**

### 3. Find Z-10 Interface 2

Look in these sections (expand them):
- **Universal Serial Bus devices**
- **Other devices**  
- **Sound, video and game controllers**

Find **"Z-10 USB Speaker (Interface 2)"** or **"HID-kompatibel leverandordefinert enhet"**

> **💡 TIP**: Look for something with a **yellow warning icon ⚠️** or **question mark ❓** - that's your LCD!

### 4. Update Driver - Manual Selection

1. **Right-click** on "Z-10 USB Speaker (Interface 2)"
2. Click **"Update driver"**
3. Click **"Browse my computer for drivers"**
4. Click **"Let me pick from a list of available drivers on my computer"**

### 5. Select Universal Serial Bus Devices

1. **UNCHECK** ☐ "Show compatible hardware"
2. In the **left list** ("Manufacturer"), scroll and click: **"(Standard USB devices)"** or **"Universal Serial Bus devices"**
3. In the **right list** ("Model"), click: **"WinUsb Device"** or **"USB Test Device"**
4. Click **Next**

### 6. Confirm Installation

- Windows will warn you about compatibility
- Click **"Yes"** or **"Install anyway"**
- Wait for installation to complete

### 7. Verify Success

After installation:
- The device should show **no warning icon**
- Status should be **"OK"** or **working**

---

## Screenshot Guide

I'll create screenshots to show you exactly what to click:

1. Device Manager → View menu
2. The list showing "Z-10 USB Speaker (Interface 2)"
3. The driver selection window with "WinUsb Device"

---

## If You Can't Find Interface 2

If you don't see "Z-10 USB Speaker (Interface 2)", look for:
- Any device with **yellow warning ⚠️** under USB or Other Devices
- **"Unknown device"** with Hardware ID containing `046D` and `0A07`
  - Right-click → Properties → Details tab → Hardware Ids

---

## After Installation

Once the driver is installed, run this to test:

```powershell
& "c:\Users\Igland\logitech z-10\test_winusb_install.ps1"
```

Then try LCDHost:

```powershell
& "c:\Users\Igland\logitech z-10\LCDHost\bin\LCDHost.exe"
```

---

## Need Help Finding It?

Take a screenshot of your Device Manager window and I'll point out exactly which device to select!
