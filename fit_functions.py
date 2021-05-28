#!/usr/bin/env python3

import numpy as np

def omega_z(params, z):
	"""Beam Radii Function to be fitted, according to https://docs.scipy.org/doc/scipy/reference/odr.html

	Parameters
	----------
	params : array_like
		rank-1 array of length 4 where ``beta = array([w_0, z_0, M_sq, lmbda])``
	z : array_like
		rank-1 array of positions along an axis

	Returns
	-------
	y : array_like
		Rank-1, calculated beam-radii of a single axis based on given parameters

	"""

	w_0, z_0, M_sq, lmbda = params
	return np.sqrt(
		w_0**2 * (
			1 + ((z - z_0)**2)*((
				(M_sq * lmbda)/
				(np.pi * (w_0**2))
			)**2)
		)
	)