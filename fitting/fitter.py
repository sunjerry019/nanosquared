#!/usr/bin/env python3

import sys, os
from typing import Tuple
from matplotlib.figure import Figure
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import numpy as np
import scipy.odr
import warnings
# from overrides import overrides, EnforceOverrides # https://github.com/mkorpela/overrides

import fitting.fit_functions as fit_functions

import matplotlib.pyplot as pyplot

class ODRFitter():
    """The ODRFitter class fits the given data using scipy.odr

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
    func : function
        fcn(beta, x) --> y

    Attributes
    ----------
    model : scipy.odr.Model Instance

    data : scipy.odr.RealData Instance

    odr : scipy.odr.ODR Instance

    output : scipy.odr.Output instance

    
    """

    def __init__(self, x, y, xerror, yerror, func):
        self.model = scipy.odr.Model(func)

        self.data = None
        self.loadData(x, y, xerror, yerror)

        self.odr    = None
        self.output = None

        self.figure = None
        self.axis   = None

    def loadData(self, x, y, xerror, yerror):
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
        self.output : scipy.odr.Output instance
            This object is also assigned to the attribute .output of Fitter
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.odr.Output.html

            In particular:
                self.output.res_var = chi_sq_red // https://arxiv.org/abs/1012.3754
                self.output.beta    = Estimated parameter values
                self.output.sd_beta = Standard deviations of the estimated parameters
                self.output.info    = Reason for returning, as output by ODRPACK (cf. ODRPACK UG p. 38).
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

    def predict(self, x):
        """Predicts the `y` values based on the fitted result. 

        Parameters
        ----------
        x : array_like
            Values to predict

        Returns
        -------
        y : array_like
            Predicted Values

        """
        if self.output is None:
            raise RuntimeWarning(".fit() has not been run. Please run .fit() before running predict()")
        
        return self.model.fcn(self.output.beta, x)

    def getPlotOfFit(self, numpoints: int = 4096) -> Tuple[pyplot.Figure, pyplot.Axes]:
        """Plots the fitted function with the original data.
        Opens a `matplotlib` figure to achieve this.

        Returns the `matplotlib` figures and axes.

        Parameters
        ----------
        numpoints : int, optional
            Number of data points along the x-axis, by default 4096

        """

        if self.output is None:
            raise RuntimeWarning(".fit() has not been run. Please run .fit() before running getPlotOfFit()")

        _min_x, _max_x = self.data.x.min(), self.data.x.max()
        _x = np.linspace(_min_x, _max_x, num = numpoints, endpoint = True)
        _y = self.predict(_x)

        # self.figure = pyplot.figure()
        # self.axis   = self.figure.add_subplot(1,1,1) 

        self.figure, self.axis = pyplot.subplots(1, 1) # nrow, ncol, position

        self.axis.set_title("Fitted Plot")        
        self.axis.plot(self.data.x, self.data.y, marker = '+')
        self.axis.plot(_x         , _y         , linestyle = "-", label = "Fit")
        self.axis.legend()

        return self.figure, self.axis
        

    

class MsqFitter(ODRFitter):
    """Class to fit for an M_Squared using fit_functions.omega_z (Guassian Beam Profile function) using ODR,

    By default, initial guesses for w_0 and z_0 are 1.
    Use self.estimateInitialGuesses() to estimate w_0, z_0

    Note that the fit function is normalized if:
	- Everything is in SI-Units, or
	- w, w_0: [um], z, z_0: [mm], lmbda: [nm]

    Using the second case seem to be more numerically stable.

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
    wavelength : float_like
        Wavelength of the laser, to be given manually for fitting
    wavelength_err : float_like, optional
        Error of the wavelength of the laser, to be used in error propagation to find the m_squared
        By default: 0

    Attributes
    ----------
    model : scipy.odr.Model Instance

    data : scipy.odr.RealData Instance

    odr : scipy.odr.ODR Instance

    output : scipy.odr.Output instance
    
    wavelength : array_like of rank 2
        [wv, wv_err] - wavelength of the data and its corresponding error
    initial_guesses : array_like
        initial_guesses for the fit
    m_squared : array_like
        ``np.array([m_squared, m_squared_err])`` of floats; calculated m_squared based on self.wavelength and the fit

    """
    def __init__(self, x, y, xerror, yerror, wavelength: float, wavelength_err: float = 0):        
        # NOTE: To use ``fit_functions.omega_z`` as a default value in a function: https://stackoverflow.com/a/41921291

        self.wavelength      = np.array([wavelength, wavelength_err], dtype= np.float64)
        self.initial_guesses = np.array([1  , 1  , wavelength], dtype = np.float64)
        #                                w_0, z_0, M_sq_lmbda

        self._m_squared_calculated = False
        self._m_squared            = None

        super().__init__(x, y, xerror, yerror, fit_functions.omega_z)

    @property
    def m_squared(self):
        """Getter for the m_squared value

        Returns
        -------
        m_squared : array_like of length 2
            np.array([m_squared, m_squared_err]) of floats
            Value of the fitted m_squared and its corresponding error

        Raises
        ------
        RuntimeWarning
            Raised if .fit() has not been run.

        """

        if self.output is None:
            raise RuntimeWarning(".fit() has not been run. Please run .fit() before getting m_squared")
    
        if not self._m_squared_calculated:
            # m_squared has not been calculated for the current fit

            m_sq = self.output.beta[2] / self.wavelength[0]
            m_sq_error = m_sq * np.sqrt(
                    (self.output.sd_beta[2]/self.output.beta[2]) ** 2 +
                    (self.wavelength[1]    /self.wavelength[0] ) ** 2 
                )

            # Error propagation with gauss method
            # delta M / M = sqrt((delta b/b)^2 + (delta l/l)^2)

            self._m_squared = np.array([m_sq, m_sq_error], dtype = np.float64)
            self._m_squared_calculated = True

        # Check for stopping reason
        #    1 : sum of squares convergence
        #    2 : parameter convergence
        #    3 : both of sum of squares and parameter convergence
        #    4 : iteration limit reached
        # >= 5 : questionable results or fatal errors detected

        if (self.output.info >= 4):
            warnings.warn("Fit is dubious. Reasons for convergence:\n\t{}".format('\n\t'.join(self.output.stopreason)))
        
        return self._m_squared
    
    def setInitialGuesses(self, w_0 : float = 1, z_0 : float = 1):
        """Sets the initial guesses

        Parameters
        ----------
        w_0 : float, optional
            Guess for beam waist radius, by default 1
        z_0 : float, optional
            Guess for focal point position, by default 1

        """

        self.initial_guesses[0:2] = [w_0, z_0]

    def estimateInitialGuesses(self):
        """Estimates the initial parameters w_0, z_0 from the data given using the minimum y-value and save it into self.initial_guesses.
        """

        min_w = np.argmin(self.data.y)

        z_0 = self.data.x[min_w]
        w_0 = self.data.y[min_w]

        self.setInitialGuesses(w_0 = w_0, z_0 = z_0)
    
    def fit(self):
        """Fits using self.initial_guesses and ODRFitter.fit()

        Returns
        -------
        self.output : Output instance
            See ODRFitter.fit() for more information

        """
        self._m_squared_calculated = False

        return super().fit(initial_params = self.initial_guesses)

    def estimateAndFit(self):
        """Equivalent to running ``estimateInitialGuesses()`` then ``fit()``

        Returns
        -------
        self.output : Output instance
            See ODRFitter.fit() for more information

        """
        self.estimateInitialGuesses()
        return self.fit()

if __name__ == "__main__":
    import code; code.interact(local=locals())
