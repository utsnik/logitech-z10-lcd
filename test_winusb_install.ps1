# Quick Test: Can We Access Z-10 LCD via WinUSB Now?

Write-Host "=== Testing Z-10 LCD Access ===" -ForegroundColor Cyan
Write-Host ""

# Check if Interface 2 has WinUSB driver
Write-Host "Checking Interface 2 driver status..." -ForegroundColor Yellow

$interface2 = Get-PnpDevice | Where-Object { 
    $_.InstanceId -like "*046D*0A07*MI_02*" 
} | Select-Object -First 1

if ($interface2) {
    Write-Host "Device: $($interface2.FriendlyName)" -ForegroundColor White
    Write-Host "Status: $($interface2.Status)" -ForegroundColor $(if ($interface2.Status -eq "OK") { "Green" }else { "Yellow" })
    
    # Check what driver is being used
    $driver = Get-PnpDeviceProperty -InstanceId $interface2.InstanceId -KeyName "DEVPKEY_Device_Service" -ErrorAction SilentlyContinue
    
    if ($driver) {
        Write-Host "Driver Service: $($driver.Data)" -ForegroundColor Cyan
        
        if ($driver.Data -eq "WinUSB") {
            Write-Host ""
            Write-Host "✓ SUCCESS! WinUSB driver is installed!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Next step: Test with LCDHost" -ForegroundColor Yellow
            Write-Host "Run: & 'c:\Users\Igland\logitech z-10\LCDHost\bin\LCDHost.exe'" -ForegroundColor Gray
        }
        else {
            Write-Host ""
            Write-Host "⚠ Driver is: $($driver.Data), not WinUSB" -ForegroundColor Yellow
            Write-Host "Need to manually update driver in Device Manager" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "Could not determine driver service" -ForegroundColor Red
    }
}
else {
    Write-Host "Interface 2 not found!" -ForegroundColor Red
    Write-Host "Make sure Z-10 is plugged in" -ForegroundColor Yellow
}

Write-Host ""
