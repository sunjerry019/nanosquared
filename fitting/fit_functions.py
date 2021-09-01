#!/usr/bin/env python3

import numpy as np

from typing import Callable

def convertODRtoOCF(func):
	"""Generates a function for scipy.optimize.curve_fit based on a scipy.odr function

	Parameters
	----------
	func : function
		fcn(beta, x) --> y

	Returns
	-------
	func : function
		fcn(x, *beta) --> y

		where beta = paramaters

	"""
	def newFunc(x, *args):
		return func(args, x)

	# newFunc.__name__ = func.__name__ doesn't work and its not important
	
	return newFunc

def omega_z(params, z):
	"""Beam Radii Function to be fitted, according to https://docs.scipy.org/doc/scipy/reference/odr.html

	Beam Radii to be the HALF of the D4Sigma definition of beam width.

	Note that this function is normalized if:
	- Everything is in SI-Units, or
	- w, w_0: [um], z, z_0: [mm], lmbda: [nm]

	Parameters
	----------
	params : array_like
		rank-1 array of length 3 where ``beta = array([w_0, z_0, M_sq_lmbda])``
	z : array_like
		rank-1 array of positions along an axis

	Returns
	-------
	y : array_like
		Rank-1, calculated beam-radii of a single axis based on given parameters

	"""

	w_0, z_0, M_sq_lmbda = params
	return w_0 * np.sqrt(
		1 + ((z - z_0)**2)*((
			(M_sq_lmbda)/
			(np.pi * (w_0**2))
		)**2)
	)

def omega_z_lambda(wavelength: float):
	"""Returns a w_0 Function to be fitted, according to https://docs.scipy.org/doc/scipy/reference/odr.html that has wavelength already included

	Refer to fit_functions.omega_z for documentation

	Parameters
	----------
	wavelength : float
		Wavelength to be used for the M^2 Fit

	Returns
	-------
	func : f(params, z) -> y
		omega_z function that has lambda included

	"""
	
	def omega_z(params, z):
		w_0, z_0, M_sq = params
		
		return w_0 * np.sqrt(
			1 + ((z - z_0)**2)*((
				(M_sq * wavelength)/
				(np.pi * (w_0**2))
			)**2)
		)

	return omega_z