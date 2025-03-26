import os
os.environ["SD_ENABLE_ASIO"] = "1"
import sounddevice as sd
import logging
import queue
import sys
import numpy as np
import sounddevice as sd
import soundfile as sf


audioqueue = queue.Queue()

audiovus=queue.Queue()

def audioqueue_callback(indata, frames, time, status):
    """
    Callback function for the sounddevice InputStream.

    This function is called by the sounddevice library for each audio block received.
    It puts the audio data into the audioqueue and the maximum absolute value of the audio data into the audiovus queue.

    Args:
        indata (numpy.ndarray): The audio data block.
        frames (int): The number of frames in the audio data block.
        time (sounddevice.CallbackTimeInfo): Time information about the audio stream.
        status (sounddevice.CallbackFlags): Status flags for the audio stream.

    """
    global audioqueue
    global audiovus
    """This is called (from a separate thread) for each audio block."""
    if status:
        logging.error(f"CALLBACK ERROR: {status}" )
    audioqueue.put(indata.copy())
    audiovus.put(np.abs(np.max(indata, axis=0)))


def record_loop(device , filename, channels):
    """
    Main loop for recording audio.

    This function sets up the audio stream and continuously records audio data to a file.
    It listens for a 'stop' message in the audioqueue to terminate the recording.

    Args:
        device (int or str): The audio device to use for recording.
        filename (str): The name of the file to record to.
        channels (int): The number of audio channels to record.

    Raises:
        Exception: If an unexpected string is received in the audioqueue.
    """
    logging.info(f"RECORDING Starting recording to {filename} with device={device} and channels={channels}")
    global audioqueue

    logging.info(f"RECORDING Supported OGG subTypes: {sf.available_subtypes('OGG')}")

    ## reasonable defaults...
    samplerate=48000
    ## bsize=2048  ## 42ms @ 48kHz

    subtype="Opus"


    # Make sure the file is opened before recording anything:
    with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                    channels=channels, subtype=subtype) as file:
        with sd.InputStream(samplerate=samplerate, device=device,
                           ## blocksize=bsize, 
                            channels=channels, callback=audioqueue_callback):
            while True:
                msg=audioqueue.get()
                
                if isinstance(msg,str):
                    if msg=='stop': 
                        break
                    else:
                        logging.error(f"Unexpected string in audioqueue: {msg}")
                        continue

                file.write(msg)

    logging.info("RECORDING: thread exit!")
