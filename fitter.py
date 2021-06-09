#!/usr/bin/env python3

import numpy as np
import scipy.odr

import fit_functions

class ODRFitter():
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

class MsqFitter(ODRFitter):
    """Class to fit for an M_Squared using fit_functions.omega_z (Guassian Beam Profile function),

    By default, initial guesses for w_0 and z_0 are 1.
    Use self.estimateInitialGuesses() to estimate w_0, z_0

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

    Attributes
    ----------
    model : scipy.odr.Model Instance
    data : scipy.odr.RealData Instance
    odr : scipy.odr.ODR Instance
    output : scipy.odr.Output instance
    wavelength : float_like
        wavelength of the data
    initial_guesses : array_like
        initial_guesses for the fit
    m_squared : array_like
        ``np.array([m_squared, m_squared_err])`` of floats; calculated m_squared based on self.wavelength and the fit

    """
    def __init__(self, x, y, xerror, yerror, wavelength):        
        # NOTE: To use ``fit_functions.omega_z`` as a default value in a function: https://stackoverflow.com/a/41921291

        self.wavelength      = wavelength
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

            m_sq = self.output.beta[2] / self.wavelength
            m_sq_error = 1

            # TODO: implement the error propagation

            self._m_squared = np.array([m_sq, m_sq_error], dtype = np.float64)
            raise NotImplementedError()

        return self._m_squared
            

    def estimateInitialGuesses(self):
        """Estimates the initial parameters w_0, z_0 from the data given using the minimum y-value and save it into self.initial_guesses.
        """

        min_w = np.argmin(self.data.y)

        z_0 = self.data.x[min_w]
        w_0 = self.data.y[min_w]

        self.initial_guesses[0:2] = [w_0, z_0]
    
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
