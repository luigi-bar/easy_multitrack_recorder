import os
os.environ["SD_ENABLE_ASIO"] = "1"

from ui import EasyMTRui
from audiodevice import AudioDevice
import time
from tkinter import ttk
import tkinter as tk
import sounddevice as sd
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout)

if __name__ == "__main__":
    logging.info("EASY MULTITRACK RECORDING Starting")
    ui = EasyMTRui()
    ui.mainloop()
