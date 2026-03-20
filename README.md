# 🚀 Logitech Z-10 LCD Revival

Modern, high-performance driver and plugin system for the legendary Logitech Z-10 speakers. Bypasses the dead Logitech software to provide real-time stats, weather, and more on your LCD.

---

## ⚡ Quick Start (Recommended)

1.  **Download the latest [Z10_LCD_Plugin.zip](https://github.com/utsnik/logitech-z10-lcd/releases)**.
2.  Unzip to a folder.
3.  Run **`setup.exe`**:
    *   It will install the app to `C:\Program Files\LogitechZ10`.
    *   It will automatically set up **Auto-Start with Windows**.
    *   It will guide you through the **Zadig Driver** setup if needed.

---

## 🔌 Included Plugins
1.  **Clock**: Big font Time/Date. Button 1 toggles a built-in Stopwatch.
2.  **Media Info**: "Now Playing" with smooth 50 FPS scrolling (Spotify, YouTube, Chrome, etc.).
3.  **Weather**: Real-time conditions (Auto-fetched from OpenMeteo).
4.  **System Monitor**: 4 pages of hardware stats (CPU/GPU load, temps, network, and disk).
5.  **Game Stats**: Real-time FPS & Frametime (Syncs with RivaTuner/RTSS). 
    *   *Features: Auto-app detection, Alt-Tab persistence, and EXE filtering.*

---

## 🛠️ Hardware Driver Setup
Windows 10/11 requires the **WinUSB** driver to talk to the Z-10.
1.  Open **Zadig** (included in the ZIP).
2.  Go to **Options** -> **List All Devices**.
3.  Select **Logitech Z-10 USB Speaker (Interface 2)**.
4.  Select **WinUSB** and click **Replace Driver**.

---

## 💻 Developer Setup (Run from Source)
If you want to modify the code or add your own plugins:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup libusb**:
   Place `libusb-1.0.dll` in the root folder.
3. **Run**:
   ```bash
   python z10_app.py
   ```
4. **Build**:
   Run `BUILD_EXE.bat` to generate the standalone `.exe` and installer.

---

## 🕹️ Controls
- **Display Button (Short Press)**: Cycle through plugins.
- **Display Button (Long Press 2s)**: Exit the application.
- **Buttons 1-4**: Context-specific (e.g., Button 1 toggles Stopwatch in Clock).

---

## 🛠️ Troubleshooting
- **LCD is blank**: Ensure you've performed the Zadig driver swap on **Interface 2**.
- **FPS is 0**: Ensure RivaTuner Statistics Server (RTSS) is running.
- **Media info missing**: Check if you have the proper Windows media overlay enabled.
