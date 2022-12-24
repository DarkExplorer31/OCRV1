import cx_Freeze 
import sys 
import os
import os.path
import re

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [cx_Freeze.Executable('OCR.V3.py',base=base)]

cx_Freeze.setup(
        name = "Programme d'OCR",
        version='0.1',
        executables= executables,
        options = {"build_exe":{"packages":["tkinter","re","os","pytesseract","pickle","tkinter.messagebox","pdf2image","subprocess","cv2","subprocess"],
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6'),
            os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6'),
        ]
    }}
    )