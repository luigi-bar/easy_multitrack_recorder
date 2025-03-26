
import os
os.environ["SD_ENABLE_ASIO"] = "1"
import sys
import logging
import sv_ttk
import sounddevice as sd
import tkinter as tk
from tkinter import ttk
import time

from audiodevice import AudioDevice
from ui import EasyMTRui

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout)



if __name__ == "__main__":
    logging.info("EASY MULTITRACK RECORDING Starting")
    ui = EasyMTRui()
    
    sv_ttk.set_theme("dark")
    ui.mainloop()
