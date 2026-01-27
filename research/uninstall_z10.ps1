# Uninstall Z-10 Speakers and Reset USB Device
# This will remove all Z-10 drivers and let Windows reinstall them fresh

Write-Host "=== Z-10 USB Speaker Uninstaller ===" -ForegroundColor Cyan
Write-Host ""

# Get all Z-10 devices
$z10Devices = Get-PnpDevice | Where-Object { $_.InstanceId -like "*046D*0A07*" }

if ($z10Devices.Count -eq 0) {
    Write-Host "No Z-10 devices found. Make sure speakers are plugged in." -ForegroundColor Yellow
    exit
}

Write-Host "Found $($z10Devices.Count) Z-10 device(s):" -ForegroundColor Green
foreach ($device in $z10Devices) {
    Write-Host "  - $($device.FriendlyName)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "This will UNINSTALL all Z-10 devices and their drivers." -ForegroundColor Yellow
Write-Host "Audio will stop working until you unplug and replug the speakers." -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "Continue? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Cancelled." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Uninstalling Z-10 devices..." -ForegroundColor Cyan

foreach ($device in $z10Devices) {
    Write-Host "  Removing: $($device.FriendlyName)" -ForegroundColor Gray
    
    # Remove device
    pnputil /remove-device $device.InstanceId 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✓ Removed" -ForegroundColor Green
    }
    else {
        Write-Host "    ⚠ Could not remove (may need admin rights)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=== Cleanup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Unplug the Z-10 USB cable" -ForegroundColor White
Write-Host "2. Wait 5 seconds" -ForegroundColor White
Write-Host "3. Plug the Z-10 USB cable back in" -ForegroundColor White
Write-Host "4. Wait for Windows to reinstall drivers (you'll hear the USB connect sound)" -ForegroundColor White
Write-Host "5. Then try Zadig again" -ForegroundColor White
Write-Host ""
