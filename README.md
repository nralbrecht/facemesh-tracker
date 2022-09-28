# FaceMesh Face Tracker

This is a Python script dedicated to track the head movement of a person in front of a webcam. To extract the movement data the webcam video the [MediaPipe Face Mesh](https://google.github.io/mediapipe/solutions/face_mesh.html) machine learning model is used. The tracking data is then provided for other applications via UDP and for example can be used to control head movement in a game.

## Installation

### 1. Install Python
[Install Python 3](https://www.python.org/downloads/). Make shure that the `python` and `pip` executables are added to the path environment variable. In most cases the installer takes care of this.

### 2. Download this Project
You can either use `git` to clone the repository or download the *FaceMesh Tracker* as a `.zip`. The newest release can be found on the [release page](https://github.com/nralbrecht/facemesh-tracker/releases).

### 3. Install Python Packages
Open a terminal in the root directory of the project and run the following commands.
```
pip install -r requirements.txt
python cmd.py --host localhost --port 4242 --video --client udp
```

### 4. Setup Tracking Software
The *FaceMesh Tracker* is ment as a headtracking data provider that can be used in other application. The following apps are confirmed to work with the *FaceMesh Tracker*:

- [**OpenTrack**](https://github.com/opentrack/opentrack)
- [**FaceTrackNoIR**](http://www.facetracknoir.nl/home/default.htm)

The data is sent using a the UDP network protocol. Choose the `UDP over Network` input when setting up the tracker. Make shure that the port is `4242` or as otherwise configured when starting the *FaceMesh Tracker*.

### 5. Setup Ambisonics rotation plugins
The IEM and SPARTA audio plugin suites support Ambisonics field rotation, using a simple /ypr OSC message. The default OSC port is 9000.

## Usage
```
# python cmd.py --help
usage: cmd.py [-h] [--host HOST] [-p PORT] [-v] [--verbose] -c {udp,osc,ypr}

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           udp server hostname
  -p PORT, --port PORT  udp server port
  -v, --video           show a live video preview of the tracking results
  --verbose             enable verbose ouput
  -c {udp,osc}, --client {udp,osc,ypr}
                        choose client implementation
```

## PipEnv
You can optionally also use PipEnv to manage a virtual environment and all packages.

```
pip install --user pipenv
pipenv install
pipenv run python cmd.py --client udp
```
