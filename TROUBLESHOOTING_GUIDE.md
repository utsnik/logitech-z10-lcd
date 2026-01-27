# Logitech Z-10 Troubleshooting Guide for Windows

## Quick Checklist

### Step 1: Physical Connection
- [ ] Plug the Z-10 USB cable directly into a **motherboard USB port** (not a hub or front panel)
- [ ] Try different USB ports on your computer
- [ ] Listen for the Windows "device connected" sound
- [ ] Check if the speakers power on (LED indicators)

### Step 2: Check Device Manager
1. Press `Win + X` and select **Device Manager**
2. Look under these sections:
   - **Sound, video and game controllers**
   - **Universal Serial Bus controllers**
3. Look for:
   - "Logitech Z-10" or
   - "USB Audio Device" or
   - Any devices with a yellow warning icon

**If you see a yellow warning:**
- Right-click the device → **Uninstall device** (check "Delete driver")
- Disconnect speakers, restart PC, reconnect speakers

### Step 3: Set as Default Audio Device
1. Right-click the speaker icon in your taskbar
2. Click **"Sound settings"** or **"Open Sound settings"**
3. Under **Output**, select the Logitech Z-10 as your default device
4. Test the sound using the **"Test"** button

### Step 4: Run Windows Audio Troubleshooter
1. Go to `Settings` → `System` → `Troubleshoot` → `Other troubleshooters`
2. Run **"Playing Audio"** troubleshooter
3. Follow the on-screen instructions

### Step 5: Update/Reinstall Drivers
**Option A: Let Windows find drivers**
1. Open Device Manager
2. Right-click on the Z-10 device
3. Select **"Update driver"**
4. Choose **"Search automatically for drivers"**

**Option B: Manual reinstall**
1. Device Manager → Right-click device → **"Uninstall device"**
2. Check **"Attempt to remove the driver for this device"**
3. Restart your computer
4. Reconnect the speakers (Windows will auto-install drivers)

### Step 6: Disable USB Power Saving
1. Press `Win + R`, type `powercfg.cpl`, press Enter
2. Click **"Change plan settings"** next to your active power plan
3. Click **"Change advanced power settings"**
4. Expand **"USB settings"** → **"USB selective suspend setting"**
5. Set to **"Disabled"** for both battery and plugged in
6. Click **Apply** and **OK**

### Step 7: Check USB Controller in Device Manager
1. Device Manager → Expand **"Universal Serial Bus controllers"**
2. Right-click each **"USB Root Hub"** → **Properties**
3. Go to **Power Management** tab
4. **Uncheck** "Allow the computer to turn off this device to save power"
5. Repeat for all USB Root Hubs

---

## Common Issues and Solutions

### Issue: "USB Device Not Recognized"
**Solutions:**
- Try a different USB cable if possible
- Test speakers on another computer to rule out hardware failure
- Update motherboard chipset drivers from manufacturer's website

### Issue: No Sound Output
**Solutions:**
- Check volume isn't muted in Windows Sound mixer
- Verify the Z-10 is set as the default playback device
- Check the physical volume knob on the speakers

### Issue: Speakers Keep Disconnecting
**Solutions:**
- Disable USB selective suspend (see Step 6)
- Update USB controller drivers
- Try a powered USB hub

---

## About the LCD Display

> **⚠️ Important:** The interactive LCD display features of the Z-10 relied on Logitech's SetPoint software, which is **no longer supported** on Windows 10/11. While basic audio should work, the LCD functionality (showing track info, visualizations, etc.) will likely not work without significant effort.

### LCD Options (Advanced):
1. **Community drivers**: Search GitHub/forums for community-made drivers
2. **Virtual machine**: Run old Windows XP/Vista in a VM with the original software
3. **Reverse engineering**: This would require custom driver development (complex)

---

## Testing Command

Once you think the speakers are working, test with this PowerShell command:

```powershell
# List all audio devices
Get-CimInstance Win32_SoundDevice | Select-Object Name, Status, StatusInfo
```

Expected output should show your Z-10 with Status "OK"

---

## Need More Help?

If none of these steps work:
1. Post the output of Device Manager (screenshot)
2. Run the PowerShell command above and share results
3. We can investigate USB descriptors or attempt custom driver development
