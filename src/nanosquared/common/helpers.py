#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir) 

import logging
logging.captureWarnings(True)

class LoggerMixIn():
	LOGLEVEL_THRESHOLD = logging.DEBUG
	
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

	def log(self, msg: str, loglevel: int = logging.INFO, end: str = "\n"):
		"""Handles the logging to easily switch between different ways of handling

		Parameters
		----------
		msg : str
			The log message
		loglevel : int
			enum in https://docs.python.org/3/library/logging.html#logging-levels,
			see https://github.com/python/cpython/blob/d730719b094cb006711b1cd546927b863c173b31/Lib/logging/__init__.py

			CRITICAL = 50
			FATAL = CRITICAL
			ERROR = 40
			WARNING = 30
			WARN = WARNING
			INFO = 20
			DEBUG = 10
			NOTSET = 0
		end : str
			Ending passed to `print`, should it print.
		"""

		logging.log(loglevel, msg)
		if loglevel >= self.LOGLEVEL_THRESHOLD:
			print(f"{logging.getLevelName(loglevel)}: {msg}", end = end)

def ensureInt(x: int):
	"""Returns `x` if it is an integer, otherwise raises TypeError

	Parameters
	----------
	x : int
		The number that must be an integer

	Returns
	-------
	x : int
		Only returns if x is an integer, otherwise raises TypeError

	Raises
	------
	TypeError
		Raised when the given number is not an integer
	"""
	# Check if integer: https://stackoverflow.com/a/48940855
	error = True
	try:
		if (int(x) == x):
			error = False
			return int(x)
	except (TypeError, ValueError):
		pass
	
	if error:
		raise TypeError(f"Given input must be an integer, got: {x}")