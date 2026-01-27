# FINAL STEP: Fixing Media Controls and LCD Glitches

## 🧪 Part 1: Fix Media Controls (Buttons)

The scan confirms that **Interface 3** (the buttons) is using the **WinUSB** driver by mistake. We need to switch it back to the default Windows HID driver.

### Direct Instructions:
1. Open **Device Manager**.
2. Go to **Universal Serial Bus devices** (look at the bottom of the list).
3. You will see **TWO** entries for "Z-10 USB Speaker...". 
4. Right-click the one that says **Interface 3**. 
   *(If you're not sure which is which, right-click -> Properties -> Details -> Hardware IDs. Look for **MI_03**)*.
5. Click **Update driver**.
6. Select **Browse my computer for drivers**.
7. Select **Let me pick from a list of available drivers...**.
8. **UNCHECK** "Show compatible hardware".
9. Select **(Standard USB Control Devices)** in the left list.
10. Select **HID-compliant consumer control device** in the right list.
11. Click **Next** and **Finish**.

**Your media controls should start working immediately!**

---

## 🎨 Part 2: Fix LCD Glitches (Blocks)

I've discovered the Z-10 expects the pixels in a slightly different order than my code was sending. This is why you see "glitchy blocks". 

I have updated the `z10_driver.py` with the corrected logic. **Once the buttons are fixed, run the monitor again and it should be crystal clear!**

```powershell
Start-Process powershell -ArgumentList "-Command python 'c:\Users\Igland\logitech z-10\z10_monitor.py'" -Verb RunAs -Wait
```
