import os
import sys

def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    When bundled, PyInstaller extracts to a temp folder and sets sys._MEIPASS.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Not bundled, use current directory or script directory
        base_path = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__ if '__main__' in sys.modules else __file__))

    return os.path.join(base_path, relative_path)
