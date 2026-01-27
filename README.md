# Logitech Z-10 LCD Driver: Installation Guide 🚀

This guide explains how to set up the Z-10 LCD Plugin System on a new machine.

## 1. Hardware Driver (The Most Important Step)
The Z-10 speakers were designed for Windows XP. To work on modern Windows, you must replace the default LCD driver with a generic WinUSB driver.

1.  Download **Zadig** from [zadig.akeo.ie](https://zadig.akeo.ie/).
2.  Plug in your Z-10 speakers.
3.  In Zadig, go to **Options** -> **List All Devices**.
4.  Select **Logitech Z-10 USB Speaker (Interface 2)**.
    *   *Note: Ensure it's Interface 2. Interface 0 and 1 are for Audio/HID Controls.*
5.  Select **WinUSB** as the driver.
6.  Click **Replace Driver**.

## 2. Software Requirements
If you are running from source, you need Python 3.10+ and the following libraries:

```bash
pip install pyusb psutil pillow pywin32
```

You also need `libusb-1.0.dll` in the same folder as `z10_app.py`.

## 3. Running the App
Simply run the main script:
```bash
python z10_app.py
```

## 4. Packing for others (Creating an .EXE)
To send this to someone who doesn't have Python installed, you can use **PyInstaller**:

1.  Install PyInstaller: `pip install pyinstaller`
2.  Run the build command:
    ```bash
    pyinstaller --onefile --noconsole --add-data "libusb-1.0.dll;." --add-data "get_media.ps1;." --add-data "plugins;plugins" z10_app.py
    ```
3.  The standalone `.exe` will be in the `dist/` folder.

## 🛠️ Troubleshooting
- **Access Denied:** Usually means another process is using the LCD. Unplug and replug the speakers.
- **Media not showing:** Ensure you are playing music in a supported app (Spotify, Chrome, YouTube, etc.).
- **GPU Stats missing:** Ensure you have NVIDIA drivers installed and `nvidia-smi` is available in your PATH.
