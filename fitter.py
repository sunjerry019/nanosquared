#!/usr/bin/env python3

import numpy as np
import scipy.odr

class Fitter():
    """The Fitter class fits the given data using scipy.odr

    Parameters
    ----------
    x : array_like
        Rank-1, Independent variable
    y : array_like
        Rank-1, Dependent variable, should be of the same shape as ``x``
    xerror : array_like or function
        Rank 1, Error in x, should be of the same shape as ``x`` or func(x) --> xerror
    yerror : array_like or function
        Rank 1, Error in y, should be of the same shape as ``y`` or func(y) --> yerror
    func : function, optional
        fcn(beta, x) --> y, by default `self.omega_z` (Guassian Beam Profile function)
    
    """

    @staticmethod
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

    def __init__(self, x, y, xerror, yerror, func = omega_z):
        self.model = scipy.odr.Model(func)

        self.data = None
        self.load_data(x, y, xerror, yerror)

        self.odr    = None
        self.output = None

    def load_data(self, x, y, xerror, yerror):
        """Load the data into a data object

        Parameters
        ----------
        x : array_like
            Rank 1, Independent variable
        y : array_like
            Rank 1, Dependent variable, should be of the same shape as ``x``
        xerror : array_like or function
            Rank 1, Error in x, should be of the same shape as ``x`` or func(x) --> xerror
        yerror : array_like or function
            Rank 1, Error in y, should be of the same shape as ``y`` or func(y) --> yerror

        """
        xerror = xerror(x) if callable(xerror) else xerror
        yerror = yerror(x) if callable(yerror) else yerror
        
        self.data = scipy.odr.RealData(x, y, sx=xerror, sy=yerror)

    def fit(self, initial_params):
        """Fit the data using the odr Model and saves the output to ``self.output``

        Parameters
        ----------
        initial_params : array_like
            Represents the initial guesses. Rank 1 Array with length equal to the number of parameters defined for self.model.For w(z): Rank 1 of length 4 with ``initial_params = array([w_0, z_0, M_sq, lmbda])``
        
        Returns
        -------
        self.output : Output instance
            This object is also assigned to the attribute .output of Fitter
        
        """

        self.odr = scipy.odr.ODR(self.data, self.model, beta0 = initial_params)
        self.output = self.odr.run()
        return self.output

    def printOutput(self):
        """Prints the output of .fit(), otherwise raises a warning

        Raises
        ------
        RuntimeWarning
            Raised if .fit() has not been run.

        """
        if self.output is not None:
            self.output.pprint()
        else:
            raise RuntimeWarning(".fit() has not been run. Please run .fit() before printing output")
    

    # TODO actually fit some data

if __name__ == "__main__":
    # f = Fitter()
    pass