# easy_multitrack_recorder# how to run from source

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

# how to build from source

first install (see above), then:

    cd src
    pyinstaller -F easy_multitrack_recorder.py --add-data "assets/*:assets" --icon "assets/icon.ico"