import serial

from scipy.fftpack import fft, fftfreq
import numpy as np

import functools
import time

class SerialCallback(object):
	""" handles serial communication and frequency analysis of a data chunk
	"""

	def __init__(self, device, samples=6):
		self.device = device
		self._samples = 6
		self._rate = None
		self._ts = None
		self._s = None
		self._counter = 0

	def __enter__(self):
		self._s = serial.Serial(self.device, 9600)
		time.sleep(3)
		print(self._s.read(self._s.inWaiting()).decode('utf-8'))
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		self._s.close()
		if exc_type != None:
			return False
		return True

	def __call__(self, data):
		if self._smoother():
			return
		vals, freqs = self.sample(data)
		vals = np.where(vals >= 255, 255, vals)
		try:
			self._write(vals)
		except:
			pass

		# printing
		pins = self._read()
		if len(pins) != 6:
			pins += [0 for i in range(6 - len(pins))]
		s = ""
		for v, f, p in zip(vals, freqs, pins):
			p = int(p)
			if v == 255:
				v = f'\033[91m{v:3.0f}\033[0m'
			else:
				v = f'{v:3.0f}'
			if p == 255:
				p = f'\033[32m{p:3.0f}\033[0m'
			else:
				p = f'{p:3.0f}'
			s += f'\033[90m{f:5.0f}\033[0m : {v} / {p} | '
		print(s[:-2])

	def _smoother(self):
		""" help to smooth the audio data a little, as it can be very noisy over small samples
		"""
		self._counter += 1
		if self._counter % 3 == 0:
			self._counter = 0
			return True
		return False

	def _write(self, vals):
		""" writes values to the serial connection
		"""
		for i in vals:
			self._s.write( chr(int(i)).encode('utf-8') )
		self._s.write('\r'.encode('utf-8'))

	def _read(self):
		""" reads from serial connection
		"""
		if self._s.inWaiting() >= 6:
			inp = self._s.read(6).decode('utf-8')
			return [str(ord(i)) for i in inp]
		else:
			return ['0' for i in range(6)]

	def sample(self, frame):
		""" fft transform into ._samples seperate samples between
		"""
		lmax = len(frame) // 2

		res = abs(fft(frame))[:lmax] / 6666
		freqs = fftfreq(frame.size, self._ts)[:lmax]
		# frequencies should be mid point
		freqs += (freqs[1] - freqs[0]) / 2
		sample = self._get_sampler(self._samples, lmax)

		# average bins
		out = []
		for i in range(self._samples - 1):
			i1 = sample[i]
			i2 = sample[i+1]
			out.append(
				np.mean(
					res[ i1 : i2 ]
				)
			)
		out.append(np.mean(
			res[ sample[-1] : -1]
		))

		return np.array(out), freqs[sample]

	@functools.lru_cache(None)
	def _get_sampler(self, samples, lmax):
		""" returns the sampling array accross the sample count
		"""
		print("DEBUG {} {}".format(samples, lmax))
		selector = np.array([i for i in range(0, samples)], dtype=float)
		s = selector.copy()
		selector = np.exp(selector)
		selector *= ((lmax - (2**7)) / max(selector))	# arbitrary value from trial and error
		selector += s
		return np.array(selector, dtype=int)

	@property
	def rate(self):
		if self._rate is None:
			raise Exception("'rate' is not defined.")
		return self._rate
	
	@rate.setter
	def rate(self, val):
		self._rate = val
		self._ts = 1.0 / val
