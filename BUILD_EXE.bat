@echo off
echo Building Z-10 LCD Standalone Executable...
pip install pyinstaller pyusb psutil pillow pywin32
pyinstaller --onefile --noconsole --add-data "libusb-1.0.dll;." --add-data "get_media.ps1;." --add-data "plugins;plugins" z10_app.py

echo.
echo Building Setup Installer...
pyinstaller --onefile --noconsole --add-data "dist\z10_app.exe;." --add-data "zadig.exe;." --add-data "libusb-1.0.dll;." --add-data "get_media.ps1;." --add-data "install_startup.bat;." setup.py

echo.
echo Packaging final ZIP...
powershell Compress-Archive -Path "dist\setup.exe", "dist\z10_app.exe", "dist\zadig.exe", "dist\install_startup.bat" -DestinationPath "Z10_LCD_Plugin.zip" -Force

echo.
echo Done! Check the 'Z10_LCD_Plugin.zip' in the root.
pause
