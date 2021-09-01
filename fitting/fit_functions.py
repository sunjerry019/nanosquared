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

def iso_omega_z(params, z):
	"""Beam Radii Function to be fitted according to ISO 11146-1:2021

	Version Referenced: BS EN ISO 11146-1:2021, equation (24) in Section 9
	Beam Diameter Definition: BS EN ISO 11145:2018, Section 3.5.2 (d4sigma)

	The original function uses the diameter, we change it to use the radii by dividing it by 2.
	We assume a stigmatic/simple astigmatic beam. 

	Parameters
	----------
	params : array_like
		rank-1 array of length 3 where ``beta = array([a, b, c])``
	z : array_like
		rank-1 array of positions along an axis

	Returns
	-------
	y : array_like
		Rank-1, calculated beam-radii of a single axis based on given parameters

	Notes
	-----
	1. From Wikipedia:  If the beam does not fill more than a third of the beam profiler's sensor area, 
		then there will be a significant number of pixels at the edges of the sensor that register a small 
		baseline value (the background value). If the baseline value is large or if it is not subtracted out 
		of the image, then the computed D4σ value will be larger than the actual value because the baseline 
		value near the edges of the sensor are weighted in the D4σ integral by x2. Therefore, baseline subtraction 
		is necessary for accurate D4σ measurements

	"""
	a, b, c = params
	return 0.5 * np.sqrt(a + b*z + c*(z**2))
