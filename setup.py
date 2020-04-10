
from setuptools import setup

setup(
	name = 'butterflies-py',
	version = '1.0.0',
	description = 'Python module for interfacing the with Butterflies-MC sketches.',
	author = 'Dustpancake',
	url = 'https://github.com/Dustpancake/Butterflies-Py',
	packages = 
		['butterflies'],
	install_requires = [
		'numpy==1.18.2',
		'PyAudio==0.2.11',
		'pyserial==3.4',
		'scipy==1.4.1'
	],
	zip_safe = False
)