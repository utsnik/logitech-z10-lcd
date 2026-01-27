# What to Type in Zadig

Based on your finding that **UAC3556B** appears on Interface 0 and 3, here's exactly what to look for:

## In Zadig's Dropdown List

When you scroll through the device list in Zadig, you want to find the entry that is:

### ✅ CORRECT - Install WinUSB Here:
```
Z-10 USB Speaker (Interface 2)
USB ID: VID_046D PID_0A07
Interface: MI_02
```

OR if you don't see "Interface 2" explicitly:

```
Z-10 USB Speaker
(The one that is NOT labeled as UAC3556B)
USB ID: 046D 0A07
```

### ❌ WRONG - Do NOT Touch These:
```
UAC3556B (Interface 0)  ← This is audio, skip it!
UAC3556B (Interface 3)  ← This is also audio, skip it!
```

---

## Visual Guide

When you select a device in Zadig's dropdown, look at the info shown:

```
Device: Z-10 USB Speaker (Interface 2)  ← Good!
USB ID: 046D 0A07                       ← Correct VID/PID
Interface: MI_02                         ← This is what we want!

Current Driver: (none) or USBCCGP
Target Driver: WinUSB (select this in right box)
```

VS

```
Device: UAC3556B (Interface 0)  ← SKIP THIS!
Device: UAC3556B (Interface 3)  ← SKIP THIS TOO!
```

---

## Can't Find Interface 2?

If Zadig doesn't show "Interface 2" as a separate option, try this:

1. Look for **multiple** "Z-10 USB Speaker" entries
2. Select each one and check the **USB ID** details
3. The one without "UAC" in the name is likely Interface 2
4. Or look for one showing `MI_02` in the instance path

---

## If Still Unsure

Take a screenshot of Zadig's dropdown list and I can help you identify which one to select!

But based on your UAC3556B finding, you want:
- **NOT** the items labeled UAC3556B
- The **other** Z-10 interface (should be Interface 2)
