import os
import sys
import ctypes
import shutil
from win32com.client import Dispatch

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def install():
    if not is_admin():
        print("Requesting Admin Privileges...")
        run_as_admin()
        sys.exit()

    print("--- Logitech Z-10 LCD Setup ---")
    
    # 1. Define Paths
    prog_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
    target_dir = os.path.join(prog_files, "LogitechZ10")
    app_data = os.getenv('APPDATA') # Still needed for shortcut path
    exe_name = "z10_app.exe"
    
    # 2. Create Directory
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created folder: {target_dir}")

    # 3. Copy Files (Assuming they are in the same folder as setup.exe)
    files_to_copy = ["z10_app.exe", "zadig.exe", "libusb-1.0.dll", "get_media.ps1"]
    for f in files_to_copy:
        if os.path.exists(f):
            shutil.copy2(f, os.path.join(target_dir, f))
            print(f"Copied {f}")
        else:
            print(f"Warning: {f} not found, skipping.")

    # 4. Create Startup Shortcut
    try:
        startup_dir = os.path.join(app_data, r"Microsoft\Windows\Start Menu\Programs\Startup")
        path = os.path.join(startup_dir, "Logitech Z-10 LCD.lnk")
        target = os.path.join(target_dir, exe_name)
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = target_dir
        shortcut.save()
        print("Startup shortcut created.")
    except Exception as e:
        print(f"Failed to create shortcut: {e}")

    # 5. Driver Check Prompt
    choice = input("\nDo you need to install the Z-10 Driver (WinUSB)? (y/n): ")
    if choice.lower() == 'y':
        zadig_path = os.path.join(target_dir, "zadig.exe")
        if os.path.exists(zadig_path):
            print("Launching Zadig...")
            os.startfile(zadig_path)
        else:
            print("Zadig.exe not found in target dir.")

    print("\nInstallation Complete!")
    input("Press Enter to finish...")

if __name__ == "__main__":
    install()
