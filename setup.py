import sys
import os
from cx_Freeze import setup, Executable


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"includes": [
    "tkinter", 
    "random", 
    "json", 
    "re",
    "urllib.request",
    "urllib.parse",
    "PIL.Image",
    "PIL.ImageTk",
    "time",
    "threading"], 

  "include_files": [
    "C:/Users/Dell/AppData/Local/Programs/Python/Python36-32/tcl/tcl8.6", 
    "C:/Users/Dell/AppData/Local/Programs/Python/Python36-32/tcl/tk8.6",
    os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
    os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
    'images/', 
    'userdata/', 
    "components/",
    "download/",
    "input-output/",
    "pages/",
    "styles/"]}
   
product_name = "Photosphere"  

dist_folder = r'[ProgramFilesFolder]'
dist_path = r'[ProgramFilesFolder]\%s' % (product_name)


os.environ['TCL_LIBRARY'] = "C:/Users/Dell/AppData/Local/Programs/Python/Python36-32/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/Users/Dell/AppData/Local/Programs/Python/Python36-32/tcl/tk8.6"

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"


shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Photosphere",           # Name
     dist_folder,              # Component_
     dist_path,# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     dist_folder,               # WkDir
     )
    ]

msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {
    'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
    'add_to_path': False,
    'initial_target_dir': dist_path
    # 'data': msi_data
    }


setup(
    name = "PhotoSphere",
    version = "1.2",
    description = "Photo Downloader",
    author= "Aditya Sriram",
    options = {"build_exe": build_exe_options},
    executables = [Executable("Photosphere.py", 
        base = base, 
        icon="images/icon_16.ico"
    )])