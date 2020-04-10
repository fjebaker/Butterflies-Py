# Butterflies-Py
Python module for interfacing the with Butterflies-MC sketches.

## Installation
This script requires the `PyAudio` package. On different operating systems, the necessary prerequisites are

- **OSX**: requires `portaudio` aswell
```bash
brew update
brew install portaudio
brew link --overwrite portaudio
```
(*todo: others*)

### Install from git
To setup, use
```bash
git clone https://github.com/Dustpancake/Butterflies-Py
cd Butterflies-Py
pip install .
```

## Running
In the current version (alpha 1.0) you'll need to have a `test.wav` in the root of the project directory, i.e. `Butterflies-Py/`. An arduino uno device running the [Butterflies-MC script](https://github.com/Dustpancake/Butterflies-MC) must be connected to the machine, and the appropriate `/dev/` used in `__main__.py`:
```python
with AudioHandler() as ah, SerialCallback('/dev/USB-DEVICE') as sc:
	ah.load_song('test.wav')
	ah.start(sc)
```

Then, starting the script is simply
```bash
python .
```