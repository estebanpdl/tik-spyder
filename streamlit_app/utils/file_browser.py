# -*- coding: utf-8 -*-

# import modules
import tkinter as tk

# import submodules
from tkinter import filedialog

def select_directory():
    """Create a directory picker dialog"""
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path