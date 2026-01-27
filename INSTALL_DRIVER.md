# Quick Start: Install WinUSB Driver for Z-10 LCD

## Step 1: Run Zadig

```powershell
# Run Zadig as Administrator
Start-Process "c:\Users\Igland\logitech z-10\zadig.exe" -Verb RunAs
```

## Step 2: Configure Zadig

1. **Enable "List All Devices"**:
   - Click **Options** → Check **"List All Devices"**

2. **Find the LCD Interface**:
   - In the dropdown, look for: **"Z-10 USB Speaker (Interface 2)"**
   - Or any entry with `046D 0A07` and `MI_02` in the details

3. **Select WinUSB Driver**:
   - In the **target driver box** (green arrow, right side)
   - Select: **WinUSB (v6.x.xxxx.xxxxx)**

4. **Install Driver**:
   - Click **"Replace Driver"** or **"Install Driver"**
   - Wait for completion (~30 seconds)

## Step 3: Verify Installation

After installation completes, check Device Manager:

```powershell
# Should show WinUSB device
Get-PnpDevice | Where-Object { 
    $_.FriendlyName -like "*Z-10*" -and 
    $_.FriendlyName -like "*Interface 2*" 
}
```

## Step 4: Test with LCDHost

1. Run LCDHost from: `c:\Users\Igland\logitech z-10\LCDHost\bin\LCDHost.exe`
2. Check if it now detects the Z-10 LCD

---

## ⚠️ Important Notes

### If Audio Stops Working
You accidentally installed the driver on Interface 0 (Audio). Fix it:
1. Open Zadig again
2. Select "Z-10 USB Speaker" (WITHOUT Interface 2 or 3)
3. Change driver back to **"USB Audio Class Driver"**

### If LCD Still Not Detected
Try Interface 3 instead:
1. Repeat the process for "Z-10 USB Speaker (Interface 3)"
2. The LCD might be on a different interface number

### Check Current Drivers
```powershell
# List all Z-10 USB devices and their drivers
Get-PnpDevice | Where-Object { $_.InstanceId -like "*046D*0A07*" } | ForEach-Object {
    $driver = Get-PnpDeviceProperty -InstanceId $_.InstanceId -KeyName "DEVPKEY_Device_DriverInfPath" 2>$null
    [PSCustomObject]@{
        Device = $_.FriendlyName
        Driver = if($driver) { $driver.Data } else { "Built-in" }
        Status = $_.Status
    }
} | Format-Table -AutoSize
```

---

## Next Steps

Once WinUSB is installed and LCDHost detects the LCD:
1. ✅ Test basic LCD functionality
2. ✅ Examine network traffic or debug logs from LCDHost
3. ✅ Start building our own Python application

If LCDHost still doesn't work, we'll reverse engineer the protocol from the DLL files!
