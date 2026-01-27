# What You're Seeing in Zadig

## UAC3556B Identification

When you plug in the Z-10 speakers, you see **UAC3556B** for:
- ✅ Interface 0 (Audio)
- ✅ Interface 3 (Also audio-related)

**UAC3556B** = USB Audio Class chip (the audio processing chip in your Z-10)

---

## What to Look For in Zadig

In Zadig's device list, you should see something like:

```
Option 1: Exact match
├── "Z-10 USB Speaker (Interface 2)"
└── Driver: (none) or USBCCGP or similar
    👈 SELECT THIS ONE!

Option 2: Without interface number
├── "Z-10 USB Speaker" (a second or third entry)
└── Driver: (none)
    👈 This might also be Interface 2

Option 3: Generic HID device
├── "USB Input Device" with VID_046D&PID_0A07
└── Check if it shows MI_02 in the details
    👈 This could be Interface 2
```

---

## What NOT to Install Driver On

**DO NOT install WinUSB on these**:
- ❌ "UAC3556B" entries
- ❌ "Z-10 USB Speaker" showing as "USB Audio Class"
- ❌ Anything showing interface 0 or 3
- ❌ Any device where the current driver is "USBSTOR" or "USBCCGP" (composite)

---

## Step-by-Step in Zadig

1. **Run Zadig as Admin** (you should have it open)

2. **Enable "List All Devices"**:
   - Menu: Options → ✅ "List All Devices"

3. **Scroll through the dropdown** and look for:
   - Any entry with "046D 0A07" in the VID/PID
   - That is **NOT** labeled as UAC3556B
   - Preferably with "(Interface 2)" in the name

4. **Select the non-audio interface**:
   - Should be the one without UAC3556B
   - Might say "Interface 2" or just be a second "Z-10" entry

5. **Choose WinUSB**:
   - Target driver (right box): **WinUSB**

6. **Replace/Install Driver**:
   - Click the button
   - Wait for success message

---

## How to Confirm You Selected the Right One

After you select a device in Zadig, look at the **USB ID** shown:
- Should show: `USB\VID_046D&PID_0A07&MI_02`
  
The **MI_02** at the end confirms it's Interface 2!

---

## If You Don't See Interface 2 Separately

Some USB composite devices don't split interfaces in Zadig. If you only see:
- UAC3556B entries (interfaces 0 & 3)
- One "Z-10 USB Speaker" composite device

Then try this:
1. Install WinUSB on the composite "Z-10 USB Speaker" device
2. This might expose the LCD interface

⚠️ **Warning**: This is riskier and might break audio temporarily. If audio stops, reinstall the "USB Audio Class" driver on it.

---

## Quick Reference

**Target Device Identifiers**:
- VID: `046D`
- PID: `0A07`
- Interface: `MI_02` (or just "not UAC3556B")

**Target Driver**: WinUSB (v6.x.xxxx)

**What to avoid**: Anything with "UAC3556B" in the name!
