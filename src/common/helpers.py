#!/usr/bin/env python3
import os,sys
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

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