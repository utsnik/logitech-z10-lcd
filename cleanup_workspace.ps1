# Cleanup Script for Logitech Z-10 Workspace
# This will remove unnecessary files while keeping essential SDK and tools

Write-Host "=== Logitech Z-10 Workspace Cleanup ===" -ForegroundColor Cyan
Write-Host ""

$baseDir = "c:\Users\Igland\logitech z-10"
$totalSaved = 0

# Function to calculate directory size
function Get-DirectorySize {
    param($path)
    if (Test-Path $path) {
        return (Get-ChildItem -Path $path -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    }
    return 0
}

# 1. Delete the LGS installer (99 MB - already extracted)
$lgsInstaller = Join-Path $baseDir "LGS_8.91.48_x64_Logitech.exe"
if (Test-Path $lgsInstaller) {
    $size = (Get-Item $lgsInstaller).Length
    Remove-Item $lgsInstaller -Force
    $totalSaved += $size
    Write-Host "✓ Deleted LGS installer" -ForegroundColor Green
    Write-Host "  Saved: $([math]::Round($size/1MB, 2)) MB" -ForegroundColor Gray
}

# 2. Delete unnecessary LGS folders
$lgsDir = Join-Path $baseDir "Logitech Gaming Software"
$foldersToDelete = @(
    "Applets",
    "ArxApplets", 
    "Drivers",
    "FWUpdate",
    "LAClient",
    "LU_1",
    "imageformats",
    "platforms"
)

foreach ($folder in $foldersToDelete) {
    $path = Join-Path $lgsDir $folder
    if (Test-Path $path) {
        $size = Get-DirectorySize $path
        Remove-Item $path -Recurse -Force -ErrorAction SilentlyContinue
        $totalSaved += $size
        Write-Host "✓ Deleted $folder/" -ForegroundColor Green
        Write-Host "  Saved: $([math]::Round($size/1MB, 2)) MB" -ForegroundColor Gray
    }
}

# 3. Delete runtime DLLs and EXEs (keep only SDK)
Write-Host "`nDeleting runtime files (keeping SDK)..." -ForegroundColor Yellow

$runtimeFiles = Get-ChildItem -Path $lgsDir -File | Where-Object { 
    $_.Extension -in @('.dll', '.exe') 
}

foreach ($file in $runtimeFiles) {
    $size = $file.Length
    Remove-Item $file.FullName -Force
    $totalSaved += $size
}

if ($runtimeFiles.Count -gt 0) {
    Write-Host "✓ Deleted $($runtimeFiles.Count) runtime files" -ForegroundColor Green
}

# 4. Delete Resources folder except Doc
$resourcesDir = Join-Path $lgsDir "Resources"
if (Test-Path $resourcesDir) {
    $docDir = Join-Path $resourcesDir "Doc"
    
    # Get all items except Doc folder
    Get-ChildItem -Path $resourcesDir | Where-Object { $_.FullName -ne $docDir } | ForEach-Object {
        $size = if ($_.PSIsContainer) { Get-DirectorySize $_.FullName } else { $_.Length }
        Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
        $totalSaved += $size
    }
    
    Write-Host "✓ Cleaned Resources folder (kept Doc/)" -ForegroundColor Green
}

# Summary
Write-Host "`n=== Cleanup Complete ===" -ForegroundColor Cyan
Write-Host "Total space saved: $([math]::Round($totalSaved/1MB, 2)) MB" -ForegroundColor Green

Write-Host "`n=== Files Kept ===" -ForegroundColor Cyan
Write-Host "✓ LCDHost/ - Complete LCD driver and tools" -ForegroundColor White
Write-Host "✓ LcdStudio_810_setup.exe - LCD studio installer" -ForegroundColor White  
Write-Host "✓ Logitech Gaming Software/SDK/ - SDK DLLs" -ForegroundColor White
Write-Host "✓ Logitech Gaming Software/Resources/Doc/ - API documentation" -ForegroundColor White
Write-Host "✓ who0p - system info/ - Reference layouts" -ForegroundColor White
Write-Host "✓ TROUBLESHOOTING_GUIDE.md - Your troubleshooting guide" -ForegroundColor White
Write-Host "✓ FILE_ANALYSIS.md - File analysis document" -ForegroundColor White

Write-Host "`n✓ Done! Workspace cleaned." -ForegroundColor Green
