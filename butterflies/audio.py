import pyaudio
import wave

import functools
import sys
import os

import numpy as np

class AudioHandler(object):
	""" class for handling playback and data reading; methods only accessible
		inside a context manager
	"""
	def __init__(self, chunk=2048):
		self._song = None
		self._format = {}
		self._p = None
		self.chunk = chunk
		self._context = False

	def _in_context(func):
		""" ensures func only callable inside a context
		"""
		@functools.wraps(func)
		def wrapper(cls, *args, **kwargs):
			if cls._context:
				return func(cls, *args, **kwargs)
			else:
				raise Exception(f'method {func} only callable inside of a context.')
		return wrapper

	def __enter__(self):
		""" entering a context allows context methods to be used and
			instantiates the audio player
		"""
		self._context = True
		self._p = pyaudio.PyAudio()
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		""" existing terminates audio player instance and removes context flag
		"""
		self._context = False
		self._p.terminate()
		if exc_type != None:
			return False
		return True

	@_in_context
	def load_song(self, path):
		""" check file exists and is wave, and store path
		"""
		if not os.path.isfile(path):
			raise Exception(f'"{path} : no such file.')
		elif os.path.splitext(path)[1] != '.wav':
			raise Exception(f'"{path}" : is not a .wav file. ')
		else:
			self._song = path
			self._describe()

	@_in_context
	def start(self, callback=None):
		""" read in properties, and begin playback. calls callback.rate = rate, and then callback(data) 
			after each consecutive write
		"""
		callback.rate = self._format['rate']
		with wave.open(self._song, 'rb') as wf:

			stream = self._p.open(**self._format)	
			data = wf.readframes(self.chunk)

			while len(data) > 0:
				stream.write(data)

				if callback is not None:
					callback(np.fromstring(data, dtype=np.short))
				data = wf.readframes(self.chunk)

			stream.stop_stream()
			stream.close()

	def _describe(self):
		""" describe the song in path
		"""
		prop = {}
		with wave.open(self._song, 'rb') as wf:
			prop['rate'] = wf.getframerate()
			prop['format'] = self._p.get_format_from_width(wf.getsampwidth())
			prop['channels'] = wf.getnchannels()
			prop['output'] = True

		self._format = prop



