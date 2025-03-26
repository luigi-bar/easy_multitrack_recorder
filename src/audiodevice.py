import os
os.environ["SD_ENABLE_ASIO"] = "1"
import sounddevice as sd
import logging

class AudioDevice:
    """
    Represents an audio device with its name, API, and maximum input channels.
    """
    def __init__(self, name, api, max_input_channels, audio_device_id):
        """
        Initializes an AudioDevice object.

        Args:
            name (str): The name of the audio device.
            api (str): The API the device belongs to (e.g., 'ASIO', 'MME').
            max_input_channels (int): The maximum number of input channels the device supports.
        """
        self.name = name
        self.api = api
        self.max_input_channels = max_input_channels
        self.audio_device_id=audio_device_id
        

    def __str__(self):
        """
        Returns a string representation of the AudioDevice.
        """
        return f"[{self.api}] {self.name} - {self.max_input_channels} ch IN" 
        
    @staticmethod
    def query_devices():
        """
        Queries and returns a dictionary of available audio input devices.

        Returns:
            dict: A dictionary where keys are device IDs and values are AudioDevice objects.
                  Only devices with at least one input channel are included.
        """
        apis=sd.query_hostapis()
        logging.info(f"Supported APIS: {apis}")
        devices=[]
        all_devices=sd.query_devices()

        for api in apis:
            apiName=api['name']
            for device_id in api['devices']:
                device=all_devices[device_id]

                max_input_channels=device['max_input_channels']
                if max_input_channels>0:
                    ad=AudioDevice(device['name'], apiName, max_input_channels, device_id)
                    logging.info(f"Found device: {ad}")
                    devices.append(ad)
                else:
                    logging.info(f"   [x] discarding device {device['name']} that has zero input ports")
        return devices
