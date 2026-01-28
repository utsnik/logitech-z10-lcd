@echo off
set "EXE_NAME=z10_app.exe"
set "SHORTCUT_NAME=Logitech Z-10 LCD.lnk"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

if not exist "%EXE_NAME%" (
    echo Error: %EXE_NAME% not found in current folder!
    echo Please run this script from the same folder as the application.
    pause
    exit /b
)

echo Installing Startup Shortcut...
echo Target: %CD%\%EXE_NAME%
echo Dest:   %STARTUP_DIR%\%SHORTCUT_NAME%

powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%STARTUP_DIR%\%SHORTCUT_NAME%');$s.TargetPath='%CD%\%EXE_NAME%';$s.WorkingDirectory='%CD%';$s.Save()"

echo.
echo Success! The app will now start automatically with Windows.
pause
