#!/usr/bin/env python3

import numpy as np
import scipy.odr

class Fitter():
	"""The Fitter class fits the given data using scipy.odr
	
	Parameters
    ----------
    x : array_like of rank-1
		Independent variable
	y : array_like of rank-1
		Dependent variable, should be of the same shape as ``x``
	xerror : array_like of rank-1
		Error in x, should be of the same shape as ``x``
	yerror : array_like of rank-1
		Error in y, should be of the same shape as ``y``
	func : function, optional
        fcn(beta, x) --> y, by default `self.omega_z` (Guassian Beam Profile function)
	"""

	def __init__(self, x, y, xerror, yerror, func = self.omega_z):
		self.model = scipy.odr.Model(self.omega_z)
		self.load_data(x, y, xerror, yerror)

	def load_data(self, x, y, xerror, yerror):
		"""[summary]

		Parameters
		----------
		x : array_like of rank-1
			Independent variable
		y : array_like of rank-1
			Dependent variable, should be of the same shape as ``x``
		xerror : array_like of rank-1
			Error in x, should be of the same shape as ``x``
		yerror : array_like of rank-1
			Error in y, should be of the same shape as ``y``

		Returns
		-------
		None

		TODO: implement function
		"""

		pass
	
	@staticmethod
	def omega_z(params, z):
		"""Beam Radii Function to be fitted, according to https://docs.scipy.org/doc/scipy/reference/odr.html

		Parameters
		----------
			params : array_like of rank-1
				rank-1 array of length 4 where ``beta = array([w_0, z_0, M_sq, lmbda])``
			z : array_like of rank-1
				rank-1 array of positions along an axis

		Returns
		-------
			y : array_like of rank-1
				Calculated beam-radii of a single axis based on given parameters
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

if __name__ == "__main__":
	f = Fitter()