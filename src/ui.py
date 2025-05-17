from audiodevice import AudioDevice
import sys
import sv_ttk
import logging
import math
from threading import Thread
import tkinter as tk
from tkinter import ttk
import os
import numpy as np
import time
os.environ["SD_ENABLE_ASIO"] = "1"
import sounddevice as sd
from audiodevice import AudioDevice
import random
import datetime
import psutil
from psutil._common import bytes2human
import recorder

class EasyMTRui:
    padding = 10

    def __init__(self):
        self.window = tk.Tk()
        
        self.set_style()

        self.window.title("EASY MULTITRACK RECORDER")
        self.all_audio_devices = AudioDevice.query_devices()
        self.recording_start = None
        self.recordbutton = None
        self.recinfo_label = None
        self.devicechoosen = None
        self.image_recF = None
        self.image_recT0 = None
        self.image_recT1 = None

        self.create_ui()
        self.window.bind("<Destroy>", self.on_destroy)

    
    def on_destroy(self,event):
        if event.widget.winfo_parent() == "":
            logging.info("program is exiting...")

            recorder.audioqueue.put("stop")
            time.sleep(2) ## give the thread some time to close the file(s)

            sys.exit(0) ## bye bye.

    def mainloop(self):
        """
        Starts the main event loop of the Tkinter application.

        This method is responsible for running the Tkinter event loop,
        which keeps the application responsive and handles user interactions
        until the application is closed.
        """
        self.window.mainloop()
        
    vuTicks=20
    vuTicksW=12
    vuTicksY=5
    vuTicksR=3
    
    
    def getasset(self, resource):
        """
        Retrieves the absolute path of a resource file located within the application's bundle directory.

        Args:
            resource (str): The name of the resource file to retrieve.

        Returns:
            str: The absolute path to the resource file.
        """
    
        bundledir=os.path.abspath(os.path.dirname(__file__))
        return os.path.join(bundledir,resource)

    def create_ui(self):
        """
        Creates and configures the user interface elements of the application.

        This method sets up the layout, widgets, and initial state of the UI.
        """

        

        ## nice logo
        logoframe=tk.Frame(self.window)
        logoframe.grid(row=1,column=0, columnspan=10) 

        ttk.Label(logoframe, text="EASY MULTITRACK RECORDER",   font=('TkFixedFont',20)).grid(
            row=1, column=2, padx=self.padding, pady=0
        )
        ttk.Label(logoframe, text='  '.join("multitrack recording made simple"),   font=('TkFixedFont',8)).grid(
            row=2, column=2, padx=self.padding, pady=0
        )
        self.imgw =  tk.PhotoImage(file=self.getasset("assets/logowave.png"))
        ttk.Label(logoframe, text='aaa', image = self.imgw).grid(
            row=1, column=0, padx=(self.padding,0), pady=0, rowspan=2)


        # Device: label
        ttk.Label(self.window, text="Device:",   font='TkFixedFont' ).grid(
            row=5, column=0, padx=self.padding, pady=self.padding
        )

        # Adding combobox drop down list
        n = tk.StringVar()
        self.devicechoosen = ttk.Combobox(
            self.window,
            width=max([len(f"{x}") for x in self.all_audio_devices]),
            textvariable=n,
            state="readonly",
        )
        self.devicechoosen["values"] = [
            f"{x}" for x in self.all_audio_devices]

        self.devicechoosen.grid(
            column=1, row=5, padx=self.padding, pady=self.padding, columnspan=8)
        self.devicechoosen.current()

        # record button
        self.recordbutton = tk.Button(
            self.window, command=self.record_startstop
        )
        self.recordbutton.grid(
            row=5, column=40, padx=self.padding, pady=self.padding, columnspan=2)

        ## vumeters
        vuframe=tk.Frame(self.window)
        vuframe.grid(row=21,column=1)

        self.levels=ttk.Label(vuframe, text="",  font='TkFixedFont')
        self.levels.grid(
            row=21, column=1, padx=0, pady=self.padding
        )
        self.levelsY=ttk.Label(vuframe, text="",  font='TkFixedFont', foreground='#F80')
        self.levelsY.grid(
            row=21, column=2, padx=0, pady=self.padding
        )
        
        self.levelsR=ttk.Label(vuframe, text="",  font='TkFixedFont', foreground='#F00')
        self.levelsR.grid(
            row=21, column=3, padx=0, pady=self.padding
        )
        self.levelsEND=ttk.Label(vuframe, text="",  font='TkFixedFont')
        self.levelsEND.grid(
            row=21, column=4, padx=0, pady=self.padding
        )
        self.recinfo_label = ttk.Label(self.window, text="",  font='TkFixedFont')
        self.recinfo_label.grid(
            row=21, column=2, padx=self.padding, pady=self.padding)
        
        self.set_recordbutton_image(False)

    def set_recordbutton_image(self,is_recording):
        """
        Sets the image of the record button based on the recording state.

        Args:
            is_recording (bool): True if recording is in progress, False otherwise.

        This method updates the record button's image to reflect whether the
        application is currently recording or not.
        """
        if self.image_recF  is None:
            self.image_recF = tk.PhotoImage(file=self.getasset("assets/recF.png"))
        if self.image_recT0  is None:
            self.image_recT0 = tk.PhotoImage(file=self.getasset("assets/recT0.png"))
        if self.image_recT1  is None:
            self.image_recT1 = tk.PhotoImage(file=self.getasset("assets/recT1.png"))

        if not is_recording:
            self.recordbutton.configure(image=self.image_recF ,border=0, relief=tk.FLAT,)
        else:
            now=int(time.time())
            if now%2==0:
                self.recordbutton.configure(image=self.image_recT0 ,border=0, relief=tk.FLAT,)
            else:
                self.recordbutton.configure(image=self.image_recT1 ,border=0, relief=tk.FLAT,)

        self.recordbutton.update()



    def update_recinfo_label(self):
        """
        Updates the recording information label with current recording details.

        This method updates the label with information such as recording duration,
        filename, file size, and disk usage. It is called periodically during
        recording to keep the information up-to-date.
        """
        if self.recording_start is not None:
            now = time.time()
            delta = int(now - self.recording_start)

            out=f"Duration: {delta//3600:02d}:{(delta//60)%60:02d}:{delta % 60:02d}\n\n"
            out += f"Filename: {self.filename}\n"
            try:
                out += "   Size : {}".format(bytes2human(os.path.getsize(self.filename)))
            except:
                out += "   Size : ???"

            out += "\n\n"

            usage = psutil.disk_usage(os.getcwd())
            out += "Disk usage:\n   Total: {}\n   Used : {}\n   Free : {} ({:.2f}%)\n".format(
                bytes2human(usage.total),
                bytes2human(usage.used),
                bytes2human(usage.free),
                int(usage.percent),
            )


            self.recinfo_label.configure(text=out)
            self.window.after(500, self.update_recinfo_label)
            self.set_recordbutton_image(True) ## blinking

    def update_levels(self):
        """
        Updates the VU meter levels based on the audio input.

        This method retrieves the latest audio levels from the recorder,
        calculates the VU meter display, and updates the UI accordingly.
        It is called periodically during recording.
        """
        if self.recording_start is None:
            return
        
        vus_list = []
        while not recorder.audiovus.empty():
            vus_list.append(recorder.audiovus.get(block=False))

        if len(vus_list)>0:
                
            
            vus_list=np.array(vus_list)
            audiovus=np.max(vus_list,axis=0)

            nch=len(audiovus)

            ## ensure fixed total len
            out="Channel levels:"
            out +="\n      "+" "*self.vuTicksW+"\n"
            outY="\n"+" "*self.vuTicksY+"\n"
            outR="\n"+" "*self.vuTicksR+"\n"
            outE="\n\n"

            for ch in range(nch):
                out += f"{ch+1:3} "
                out += '║ '

                levelDB=20*math.log10(max(audiovus[ch],1e-6))

                ## mapping db -> vu ticks:
                level=int(levelDB/2+22)
                if level>self.vuTicks-1:
                    level=self.vuTicks
                    

                if level>=0:
                    for i in range(level):
                        if i<self.vuTicksW:
                            out += '▉'
                        elif i<self.vuTicksW+self.vuTicksY:
                            outY += '▉'
                        else:
                            outR += '▉'

                out += "\n"
                outY += "\n"
                outR += "\n"
                outE += " ║\n"

            self.levels.configure(text=out)
            self.levelsY.configure(text=outY)
            self.levelsR.configure(text=outR)
            self.levelsEND.configure(text=outE)

        ## repeat:
        self.window.after(100, self.update_levels)



    def record_startstop(self):
        """
        Starts or stops the audio recording process.

        This method toggles the recording state. If recording is not in progress,
        it starts recording. If recording is in progress, it stops recording.
        It also updates the UI to reflect the current recording state.
        """
        if self.recording_start is None:

            if self.devicechoosen.current()<0:
                # user should choose a device 
                return


            # recording starts

            n = datetime.datetime.now()
            now=n.isoformat() # '2021-07-13T15:28:51.818095+00:00'
            now=now.split(".")[0].replace(":",'').replace('T','-')
            self.filename=f"rec_{now}.ogg"

            logging.info("Recording starts")
            self.devicechoosen.configure(state='disabled')
            self.recording_start = time.time()
            self.recordbutton.configure(text="recording...")
            self.set_recordbutton_image(True)
            self.update_levels()

            self.start_recording()
        
        else:
            # recording stops
            logging.info("Recording stopping")
            recorder.audioqueue.put("stop")
            self.recording_start = None
            self.recordbutton.configure(text="RECORD")
            self.devicechoosen.configure(state='readonly')
            #self.recinfo_label.configure(text='')
            self.levels.configure(text='')
            self.levelsY.configure(text='')
            self.levelsR.configure(text='')
            self.levelsEND.configure(text='')
            self.set_recordbutton_image(False)

        self.update_recinfo_label()
        self.recordbutton.update()


    def start_recording(self):
        """
        Starts the audio recording in a separate thread.

        This method initializes the audio recording process by creating a new
        thread that runs the `record_loop` function from the `recorder` module.
        It also logs the start of the recording process.
        """

        audiodevice=self.all_audio_devices[self.devicechoosen.current()]
      

        logging.info(f"Starting recording to {self.filename} with device={audiodevice}")
        

#        recorder.record_loop(  audiodevice.audio_device_id, self.filename, audiodevice.max_input_channels)

        thread = Thread(target = recorder.record_loop, args = (audiodevice.audio_device_id, self.filename, audiodevice.max_input_channels, ))
        thread.start()


    def set_style(self):
        ## some nice defaults...
        self.window.option_add("*ackgroun*", "#1c1c1c")
        self.window.option_add("*oregroun*", "white")

        ## the real theme
        try:
            sv_ttk.set_theme("dark")
        except Exception as e:
            logging.error(f"ERROR setting style: {e}")