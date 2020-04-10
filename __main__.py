from butterflies.audio import AudioHandler
from butterflies.comms import SerialCallback

with AudioHandler() as ah, SerialCallback('/dev/cu.usbmodem142301') as sc:
	ah.load_song('giant.wav')
	ah.start(sc)