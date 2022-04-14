#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import sys, os
from typing import Tuple
from matplotlib.figure import Figure
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir) 

import numpy as np
import scipy.odr
from   scipy.optimize import curve_fit
import warnings
# from overrides import overrides, EnforceOverrides # https://github.com/mkorpela/overrides

import fitting.fit_functions as fit_functions

import matplotlib.pyplot as pyplot

from collections import namedtuple

import common.helpers as h

# TODO: allow-variation:
# When the fit does not converge, or if the M^2 value does not make sense, automatically vary the
# start parameter until a reasonable result is obtained

class Fitter(h.LoggerMixIn):
    """Fitter provides the superclass for ODRFitter and OCFFitter
    """
    def __init__(self) -> None:
        self.output = None
        self.figure, self.axis = None, None
        self.data = None
        
        raise NotImplementedError

    def ensureNP(self, ref, varb):
        if not isinstance(varb, np.ndarray):
            if isinstance(varb, list):
                varb = np.array(list)
            elif isinstance(varb, (float, int)):
                varb = np.full_like(ref, varb)

        return varb

    def fit(self, initial_params):
        raise NotImplementedError

    def predict(self, x):
        raise NotImplementedError

    def printOutput(self):
        raise NotImplementedError
    
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
        self.axis.errorbar(self.data.x, self.data.y, yerr = self.data.sy, xerr = self.data.sx, linestyle = "None", marker = '+', barsabove = True)
        self.axis.plot(    _x         , _y         , linestyle = "-"   , label = "Fit")
        self.axis.legend()

        return self.figure, self.axis

class OCFFitter(Fitter):
    """The OCFFitter class fits the given data using scipy.optimize.curve_fit (OCF) and the least-squares method

    Parameters
    ----------
    x : array_like
        Rank-1, Independent variable
    y : array_like
        Rank-1, Dependent variable, should be of the same shape as ``x``
    yerror : array_like or function
        Rank 1, Error in y, should be of the same shape as ``y`` or func(y) --> yerror or scalar
    func : function
        fcn(beta, x) --> y

        This is based on scipy.odr. It will be converted to 
        a function suitable for scipy.optimize.curve_fit where necessary.

    Attributes
    ----------
    data : namedtuple
        .x = xdata
        .y = ydata
        .sy = yerror
        .sx = None

    output: namedtuple
        .beta = params
        .sd_beta = one standard deviation errors on the parameters
    
    """

    def __init__(self, x, y, yerror, func) -> None:
        self.data   = None
        self.loadData(x, y, yerror)

        self.func   = fit_functions.convertODRtoOCF(func)
        self.output = None

        self.figure = None
        self.axis   = None
    
    def loadData(self, x, y, yerror):
        """Load the data into a data object

        Parameters
        ----------
        x : array_like
            Rank 1, Independent variable
        y : array_like
            Rank 1, Dependent variable, should be of the same shape as ``x``
        yerror : array_like or function
            Rank 1, Error in y, should be of the same shape as ``y`` or func(y) --> yerror or scalar

        """
        yerror = yerror(y) if callable(yerror) else yerror
        yerror = self.ensureNP(y, yerror)

        data = {
            "x"  : x,
            "y"  : y,
            "sx" : None,
            "sy" : yerror
        }
        self.data = namedtuple("Data", data.keys())(*data.values())

    def fit(self, initial_params):
        """Fit the data using ``scipy.optimize.curve_fit()`` and saves the output to ``self.output``

        Parameters
        ----------
        initial_params : array_like
            Represents the initial guesses. Rank 1 Array with length equal to the number of parameters defined for self.model. 
            For w(z): Rank 1 of length 4 with ``initial_params = array([w_0, z_0, M_sq, lmbda])``
        
        Returns
        -------
        self.output : array_like
            Returns [optimalparams, sd_params], where sd_params = one standard deviation errors on the parameters

        Raises
        ------
        RuntimeError
            If the fit does not converge

        """
        
        popt, pcov = curve_fit(
            f = self.func, 
            xdata  = self.data.x, 
            ydata  = self.data.y, 
            p0     = initial_params, 
            sigma  = self.data.sy,
            method = 'lm',
        )

        output = {
            "beta"   : popt,
            "sd_beta": np.sqrt(np.diag(pcov))
        }

        print(popt, "\n")
        print(pcov)

        self.output = namedtuple("Output", output.keys())(*output.values())
        
        return self.output

    def printOutput(self):
        """Prints the output of .fit(), otherwise raises a warning

        Raises
        ------
        RuntimeWarning
            Raised if .fit() has not been run.

        """
        if self.output is not None:
            print("Optimized: ", self.output.beta)
            print("Errors:    ", self.output.sd_beta)
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
        
        return self.func(x, *self.output.beta)

class ODRFitter(Fitter):
    """The ODRFitter class fits the given data using scipy.odr

    Parameters
    ----------
    x : array_like
        Rank-1, Independent variable
    y : array_like
        Rank-1, Dependent variable, should be of the same shape as ``x``
    xerror : array_like or function
        Rank 1, Error in x, should be of the same shape as ``x`` or func(x) --> xerror or scalar
    yerror : array_like or function
        Rank 1, Error in y, should be of the same shape as ``y`` or func(y) --> yerror or scalar
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
            Rank 1, Error in x, should be of the same shape as ``x`` or func(x) --> xerror or scalar
        yerror : array_like or function
            Rank 1, Error in y, should be of the same shape as ``y`` or func(y) --> yerror or scalar

        """
        xerror = xerror(x) if callable(xerror) else xerror
        yerror = yerror(y) if callable(yerror) else yerror

        xerror = self.ensureNP(x, xerror)
        yerror = self.ensureNP(y, yerror)
        
        self.data = scipy.odr.RealData(x, y, sx=xerror, sy=yerror)

    def fit(self, initial_params):
        """Fit the data using the odr Model and saves the output to ``self.output``

        Parameters
        ----------
        initial_params : array_like
            Represents the initial guesses. Rank 1 Array with length equal to the number of parameters defined for self.model.
            For w(z): Rank 1 of length 3 with ``initial_params = array([w_0, z_0, M_sq_lmbda])``
        
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

class MsqFitter():
    """Superclass of all Msq Fitters

    Parameters
    ----------
    mode: int
        0: Fit using Msq*lambda as one term in the beam width equation 
        1: Fit using Msq as one term in the beam width equation, lambda directly included
        2: Fit using the ISO Method. Refer to fitting.fit_functions.iso_omega_z() for more information (Default)

        If using `mode = 0`, fits using M_sq_lambda instead of just M_sq. This allows the error of the wavelength to be taken into account.
        The ISO Fitting method also takes into account the error of the wavelength.
        If using `mode = 1`, the error of the wavelength is disregarded. 

    """
    M2LAMBDA_MODE = 0
    M2_MODE = 1
    ISO_MODE = 2

    def __init__(self, wavelength: float, wavelength_err: float = 0, mode: int = 3):
        self.mode = mode if (isinstance(mode, int) and (0 <= mode <= 2)) else None

        if self.mode is None:
            raise RuntimeError(f"Invalid Mode: {mode}")

        self.funcs = [
            fit_functions.omega_z, 
            fit_functions.omega_z_lambda(wavelength = wavelength),
            fit_functions.iso_omega_z
        ]

        self.i_params = [
            # w_0, z_0, M_sq_lmbda
            [1  , 1  , wavelength],
            # w_0, z_0, M_sq
            [1  , 1  , 1],
            # a, b, c
            [1, 1, 1]
        ]

        self.wavelength      = np.array([wavelength, wavelength_err], dtype= np.float64)
        self.initial_guesses = np.array(self.i_params[self.mode], dtype = np.float64)                 

        self._m_squared_calculated = False
        self._m_squared            = None

    def setInitialGuesses(self, w_0 : float = 1, z_0 : float = 1, M_sq: float = 1):
        """Sets the initial guesses, only for mode = 0 or 1

        Parameters
        ----------
        w_0 : float, optional
            Guess for beam waist radius, by default 1
        z_0 : float, optional
            Guess for focal point position, by default 1

        """
        if self.mode == 0 or self.mode == 1:
            self.initial_guesses = [w_0, z_0, M_sq]

        elif self.mode == 2:
            pass

    def estimateInitialGuesses(self):
        """Estimates the initial parameters w_0, z_0 from the data given using the minimum y-value and save it into self.initial_guesses.
           Only for mode = 0 or 1
        """

        if self.mode == self.M2_MODE or self.mode == self.M2LAMBDA_MODE:
            min_w = np.argmin(self.data.y)

            z_0 = self.data.x[min_w]
            w_0 = self.data.y[min_w]

            self.setInitialGuesses(w_0 = w_0, z_0 = z_0, M_sq = 1)

            # TODO: estimate M^2 here

        elif self.mode == self.ISO_MODE:
            self.mode = self.M2_MODE
            self.estimateInitialGuesses()
            self.func = fit_functions.convertODRtoOCF(self.funcs[self.mode])
            self.fit()

            w_0, z_0, Msq = self.output.beta

            c = Msq**2 * (self.wavelength[0]/(np.pi*w_0))**2
            a = w_0**2 + c*(z_0**2)
            b = -2*z_0*c
            
            self.initial_guesses = np.array([a,b,c])

            self.mode = self.ISO_MODE
            self.func = fit_functions.convertODRtoOCF(self.funcs[self.mode])
            
    
    @property
    def m_squared(self):
        return self._calc_msq()

    def _calc_msq(self):
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

            # The following is arranged according to the computation difficulty

            if self.mode == 1:
                # The fitted quantity is directly m2
                self._m_squared = np.array([self.output.beta[2], self.output.sd_beta[2]], dtype = np.float64) 

            elif self.mode == 0:
                m_sq = self.output.beta[2] / self.wavelength[0]
                m_sq_error = m_sq * np.sqrt(
                        (self.output.sd_beta[2]/self.output.beta[2]) ** 2 +
                        (self.wavelength[1]    /self.wavelength[0] ) ** 2 
                    )

                # Error propagation with gauss method
                # delta M / M = sqrt((delta b/b)^2 + (delta l/l)^2)

                self._m_squared = np.array([m_sq, m_sq_error], dtype = np.float64)

            elif self.mode == 2:
                # ISO Method

                # ISSUE HERE: ERROR TOO BIG
                # TODO

                a , b , c  = self.output.beta
                da, db, dc = self.output.sd_beta
                wv, dwv    = self.wavelength

                m_sq = (np.pi / (8 * wv)) * np.sqrt((4*a*c) - (b*b))

                _faktor = np.sqrt(4*a*c - b*b)
                dM_da   =   (np.pi * c) / (4*wv*_faktor)
                dM_db   = - (np.pi * b) / (8*wv*_faktor)
                dM_dc   =   (np.pi * a) / (4*wv*_faktor)
                dM_dwv  = - (np.pi * _faktor) / (8*wv*wv)

                arr     = np.array([dM_da * da, dM_db * db, dM_dc * dc, dM_dwv * dwv])
                m_sq_error = np.sqrt(np.sum(np.square(arr)))

                # Error propagation with gauss method
                # delta M = sqrt(sum (dM_di*DI)2)

                self._m_squared = np.array([m_sq, m_sq_error], dtype = np.float64)

            self._m_squared_calculated = True
        
        return self._m_squared

class MsqODRFitter(ODRFitter, MsqFitter):
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
    mode: int
        0: Fit using Msq*lambda as one term in the beam width equation 
        1: Fit using Msq as one term in the beam width equation, lambda directly included
        2: Fit using the ISO Method. Refer to fitting.fit_functions.iso_omega_z() for more information (Default)

        If using `mode = 0`, fits using M_sq_lambda instead of just M_sq. This allows the error of the wavelength to be taken into account.
        The ISO Fitting method also takes into account the error of the wavelength.
        If using `mode = 1`, the error of the wavelength is disregarded.  

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
    msq_lambda : bool
        Flag to fit to M_sq_lambda or M_sq 

    """
    def __init__(self, x, y, xerror, yerror, wavelength: float, wavelength_err: float = 0, mode: int = 3):          
        # NOTE: To use ``fit_functions.omega_z`` as a default value in a function: https://stackoverflow.com/a/41921291
        
        MsqFitter.__init__(self, wavelength = wavelength, wavelength_err = wavelength_err, mode = mode)
        ODRFitter.__init__(self, x, y, xerror, yerror, self.funcs[self.mode])

    @property
    def m_squared(self):
        # Check for stopping reason
        #    1 : sum of squares convergence
        #    2 : parameter convergence
        #    3 : both of sum of squares and parameter convergence
        #    4 : iteration limit reached
        # >= 5 : questionable results or fatal errors detected

        if (self.output.info >= 4):
            warnings.warn("Fit is dubious. Reasons for convergence:\n\t{}".format('\n\t'.join(self.output.stopreason)))
        
        return super()._calc_msq()
    
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

class MsqOCFFitter(OCFFitter, MsqFitter):
    """Class to fit for an M_Squared using fit_functions.omega_z (Guassian Beam Profile function) using scipy.optimize.curve_fit

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
    yerror : array_like or function
        Rank 1, Error in y, should be of the same shape as ``y`` or func(y) --> yerror
    wavelength : float_like
        Wavelength of the laser, to be given manually for fitting
    wavelength_err : float_like, optional
        Error of the wavelength of the laser, to be used in error propagation to find the m_squared
        By default: 0
    mode: int
        0: Fit using Msq*lambda as one term in the beam width equation 
        1: Fit using Msq as one term in the beam width equation, lambda directly included
        2: Fit using the ISO Method. Refer to fitting.fit_functions.iso_omega_z() for more information (Default)

        If using `mode = 0`, fits using M_sq_lambda instead of just M_sq. This allows the error of the wavelength to be taken into account.
        The ISO Fitting method also takes into account the error of the wavelength.
        If using `mode = 1`, the error of the wavelength is disregarded.  

    Attributes
    ----------
    wavelength : array_like of rank 2
        [wv, wv_err] - wavelength of the data and its corresponding error
    initial_guesses : array_like
        initial_guesses for the fit
    m_squared : array_like
        ``np.array([m_squared, m_squared_err])`` of floats; calculated m_squared based on self.wavelength and the fit
    msq_lambda : bool
        Flag to fit to M_sq_lambda or M_sq 

    """
    def __init__(self, x, y, yerror, wavelength: float, wavelength_err: float = 0, mode: int = 3):        
        # NOTE: To use ``fit_functions.omega_z`` as a default value in a function: https://stackoverflow.com/a/41921291
        
        MsqFitter.__init__(self, wavelength = wavelength, wavelength_err = wavelength_err, mode = mode)
        OCFFitter.__init__(self, x, y, yerror, self.funcs[self.mode])
    
    def fit(self):
        """Fits using self.initial_guesses and OCFFitter.fit()

        Returns
        -------
        self.output : namedtuple
            See OCFFitter.fit() for more information

        """
        self._m_squared_calculated = False

        return super().fit(initial_params = self.initial_guesses)

    def estimateAndFit(self):
        """Equivalent to running ``estimateInitialGuesses()`` then ``fit()``

        Returns
        -------
        self.output : Output instance
            See OCFFitter.fit() for more information

        """
        self.estimateInitialGuesses()
        return self.fit()

if __name__ == "__main__":
    import code; code.interact(local=locals())
