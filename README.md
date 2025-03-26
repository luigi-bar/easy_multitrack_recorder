<p align="center">
  <img src="src/assets/logo.png" alt="logo" />
</p>

# what it is

If you want a simple no-fuss program to record your multi-track audio interface or mixer, this is the tool for you!

You can use it for example with the Behringer XR 18 or similar mixers

## how many channels does it support?

As many as supported by the underlying PortAudio library, so basically unlimited :)

# usage

1. install it (see below)
1. start the app
1. choose your device
1. click the big button REC
1. when done, click the button again to stop

In the same folder where the app is located, an audio file will be created. It is a multichannel .ogg file.

# how to install from releases


# how to run from source

## linux

    python -m venv easy_mtr
    . easy_mtr/bin/activate
    python -m pip install -r requirements.txt

    cd src
    python easy_multitrack_recorder.py

## windows

    python -m venv easy_mtr
    audioenv\Scripts\activate
    python -m pip install -r requirements.txt

    cd src
    python easy_multitrack_recorder.py

## mac 

follow the same instructions as per Linux. If you get issues, please open a ticket

# how to build from source

first install (see above), then:

    cd src
    pyinstaller -F easy_multitrack_recorder.py --add-data "assets/*:assets" --icon "assets/icon.ico"