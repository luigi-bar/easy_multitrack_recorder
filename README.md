<p align="center">
  <img src="assets/logo.png" alt="logo" />
</p>

# what it is

If you want a simple no-fuss program to record your multi-track audio interface or mixer, this is the tool for you!

You can use it for example with the Behringer XR 18 or similar mixers, to record your live performances, etc. 

It displays the levels of the various channels in realtime, to help you troubleshooting connection and/or gain issues.

In the information panel the used disk space as well as the remaining free one is shown.

## how many channels does it support?

As many as supported by the underlying PortAudio library, so basically unlimited :)

## maximum duration of the recorded file?

The maximum file duration should be limited only by the available disk space on your system..

In practice I have tested it up to 2 hours with 16 channels. 

# usage

1. install it (see below)
1. start the app
1. choose your device
1. click the big button REC
1. enjoy the recording:
<p align="center">
  <img src="assets/demo.gif" alt="app running" />
</p>

When done, click the button again to stop. In the same folder where the app is located, an audio file will be created. It is a multichannel .ogg file.

# how to download / install 



# for developers

## how to run from source

### linux

    python -m venv easy_mtr
    . easy_mtr/bin/activate
    python -m pip install -r requirements.txt

    cd src
    python easy_multitrack_recorder.py

### windows

    python -m venv easy_mtr
    audioenv\Scripts\activate
    python -m pip install -r requirements.txt

    cd src
    python easy_multitrack_recorder.py

### mac 

follow the same instructions as per Linux. If you get issues, please open a ticket

## how to build from source

first install (see above), then:

    cd src
    pyinstaller -F easy_multitrack_recorder.py --add-data "assets/*:assets" --icon "assets/icon.ico"

For additional info , check the source code of the repo github actions 