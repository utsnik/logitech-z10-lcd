# Emergency USB Reset for Z-10

This script will disable and re-enable the Z-10 LCD interface to force Windows to reload the WinUSB driver cleanly.

$instanceId = (Get-PnpDevice | Where-Object { $_.FriendlyName -like "*Z-10*Interface 2*" }).InstanceId

if ($instanceId) {
    Write-Host "Found Z-10 Interface 2: $instanceId"
    Write-Host "Disabling..."
    Disable-PnpDevice -InstanceId $instanceId -Confirm:$false
    Start-Sleep -Seconds 2
    Write-Host "Enabling..."
    Enable-PnpDevice -InstanceId $instanceId -Confirm:$false
    Write-Host "Done! Now try running the 'Fill Screen' script again."
}
else {
    Write-Host "Could not find Z-10 Interface 2. Is it plugged in?"
}
