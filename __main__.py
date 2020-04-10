from butterflies.audio import AudioHandler
from butterflies.comms import SerialCallback

with AudioHandler() as ah, SerialCallback('/dev/cu.usbmodem141301') as sc:
	ah.load_song('test.wav')
	ah.start(sc)