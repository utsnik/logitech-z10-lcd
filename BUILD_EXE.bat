@echo off
echo Building Z-10 LCD Standalone Executable...
pip install pyinstaller pyusb psutil pillow pywin32
pyinstaller --onefile --noconsole --add-data "libusb-1.0.dll;." --add-data "get_media.ps1;." --add-data "plugins;plugins" z10_app.py
echo Copying Zadig...
copy zadig.exe dist\zadig.exe
echo.
echo Done! Check the 'dist' folder for z10_app.exe
pause
