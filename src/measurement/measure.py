#!/usr/bin/env python3

"""File provides the backend for the GUI. It is meant to combine all the modules together"""

import os,sys
from typing import Tuple
import numpy as np

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

from cameras.camera  import Camera
from cameras.wincamd import WinCamD

from stage.controller import Controller, GSC01

from fitting.fitter import MsqFitter, MsqOCFFitter

import logging

import measurement.errors as me

class Measurement():
    def __init__(self, 
            camera: Camera         = None, 
            controller: Controller = None,
            devMode: bool          = True
        ) -> None:
        """Backend to the GUI

        Parameters
        ----------
        camera : cameras.camera.Camera, optional
            Instance of a camera to be used, by default None
            If set to `None`, `WinCamD(devMode = devMode)` is used.
        controller : stage.controller.Controller, optional
            Instance of a `stage-controller` to be used, by default None.
            If set to `None`, `GSC01(devMode = devMode)` is used, which by default uses `stage._stage.SGSP26_200()`
        devMode: bool, optional
            If dev mode is set, all actions are simulated. This is passed on to `controller` if `controller` is set
            to `None`. 

        """

        self.devMode = devMode

        if controller is None:
            controller = GSC01(devMode = devMode)
        
        if camera is None:
            camera = WinCamD(devMode = True)
        
        assert isinstance(camera, Camera), f"Camera ({camera}) is not recognized"
        assert isinstance(controller, Controller), f"Controller ({controller}) is not recognized"

        self.controller = controller
        self.camera     = camera

        self.data = { 'x' : None, 'y': None }

        self.controller.homeStage()
        self.controller.findRange()

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        pass

    def take_measurements(self, rayleighLength: float = 15, numsamples: int = 50):
        """Function that takes the necessary measurements for M^2, automatically selects the range based
        on the given Rayleigh Length.

        Minimum Resolution for beam width for WinCamD-IR-BB = ~170 um

        According to ISO 11146-1:2021, we need to take measurements at at least 10 different z positions. Approximately 
        half of the measurements shall be distributed within one Rayleigh length on either side of the beam 
        waist, and approximately half of them shall be distributed beyond two Rayleigh lengths from the beam waist.

        This means, we need the travel range of approximately +- 3 z_0

        Parameters
        ----------
        rayleighLength : float, optional
            Rayleigh Length (z_0) in millimeter, by default 15
        numsamples : int, optional
            Number of samples to take at each point, by default 50
        """

        # Check if the rayleigh length fits the stage being used. 

        if ((self.controller.stage.travel - 10) / 2) < 3*rayleighLength:
            raise me.ConfigurationError(f"The travel range of the stage does not support the current configuration (Usable travel = {self.controller.stage.travel - 10} , z_R = {rayleighLength})")

        if not self.devMode and self.controller.stage.dirty:
            self.controller.homeStage()
        
        # initialization
        self.data = { 'x' : None, 'y': None }

        # find params
        _center    = self.find_center()
        _z_R_pulse = np.around(self.controller.um_to_pulse(um = rayleighLength * 1000)).astype(int)

        _within_points    = np.linspace(start=-_z_R_pulse, stop=_z_R_pulse, endpoint = True, num = 10, dtype = np.integer)        
        _without_points_1 = np.linspace(start=2*_z_R_pulse, stop=3*_z_R_pulse, endpoint = True, num = 5, dtype = np.integer) 
        _without_points_2 = -_without_points_1

        points  = np.concatenate([_within_points, _without_points_1, _without_points_2, [0]])
        points += _center

        points = np.sort(points, kind = 'stable')

        totalpts = len(points)
        digits   = len(str(totalpts))

        # Take the measurements
        for n, pt in enumerate(points):
            # https://stackoverflow.com/a/25293744
            self.log(f"Point [{(n+1): >{digits}}/{totalpts}]: {pt}")
            
            for ax in ['x', 'y']:
                y = self.measure_at(pos = pt, numsamples = numsamples, axis = ax)
                x = self.controller.pulse_to_um(pps = pt)

                dtpt = np.array([x, y[0], y[1]])
                
                if self.data[ax] is None:
                    self.data[ax] = dtpt
                else:
                    self.data[ax] = np.vstack((self.data[ax], dtpt))

        return self.data

    def find_center(self, axis: str = 'x', left: int = None, right: int = None) -> int:
        """Finds the approximate position of the beam waist using ternary search. 
        If `left` or `right` is set to None, the limits of the stage are taken

        Code Reference: https://en.wikipedia.org/wiki/Ternary_search

        Parameters
        ----------
        axis : str
            Can take 'x' or 'y', by default 'x'
        left : int, optional
            The smallest possible position, by default None
        right : int, optional
            The biggest possible position, by default None

        Returns
        -------
        center: int
            The approximate beam-waist position
        """

        if self.devMode:
            return 15

        if not self.controller.stage.ranged and (left is None or right is None):
            self.controller.findRange()

        if left is None and self.controller.stage.ranged:
            left = self.controller.stage.LIMIT_LOWER
        
        if right is None and self.controller.stage.ranged:
            right = self.controller.stage.LIMIT_UPPER

        default_abs_pres   = 10
        absolute_precision = default_abs_pres

        # We implement the iterative method
        while np.abs(right - left) >= absolute_precision:
            left_third  = np.around(left  + (right - left) / 3).astype(int)
            right_third = np.around(right - (right - left) / 3).astype(int)
            
            l = self.measure_at(axis = axis, pos = left_third)
            r = self.measure_at(axis = axis, pos = right_third)

            absolute_precision = np.max([l[1], r[1], default_abs_pres])

            if l[0] > r[0]:
                left = left_third
            else:
                right = right_third

        # Left and right are the current bounds; the maximum is between them
        return np.around((left + right) / 2).astype(int)
                    
    def measure_at(self, axis: str, pos: int, numsamples: int = 10):
        """Moves the stage to that position and takes a measurement for the diameter

        Parameters
        ----------
        pos : int
            Position to measure at
        numsamples: int
            Number of samples to take, by default 10

        Returns
        -------
        d4sigma : Tuple[float, float]
            d4Sigma diameter obtained in the form: [diam, delta diam]
        """
        self.controller.move(pos = pos)

        return self.camera.getAxis_avg_D4Sigma(axis, numsamples = numsamples)
       
    @staticmethod
    def get_w0_zR(diamAtLens: float, focalLength: float, wavelength: float, M2: float = 1) -> Tuple[float, float]:
        """Returns the beam waist radius and the Rayleigh length. 

        Parameters
        ----------
        diamAtLens : float
            Diameter of the beam at the lens in millimeter
        focalLength : float
            Focal length of the lens in millimeter
        wavelength : float
            Wavelength of the laser light in nanometer
        M2 : float, optional
            Estimated M^2 of the beam, by default 1

        Returns
        -------
        w0, zR : Tuple[float, float]
            Tuple with the beam waist radius and the Rayleigh length.
        """
        w0 = Measurement.beam_waist_radius(diamAtLens, focalLength, wavelength, M2)
        zR = Measurement.rayleigh_length(w0, wavelength, M2)

        return (w0, zR)

    @staticmethod
    def rayleigh_length(waistRadius: float, wavelength: float, M2: float = 1) -> float:
        """Calculates the Rayleigh leight given the following parameters

        Reference: https://www.rp-photonics.com/rayleigh_length.html

        Parameters
        ----------
        waistRadius : float
            Beam waist radius in um.
        wavelength : float
            Wavelength of the light used in nm.
        M2 : float, optional
            Estimated M^2 of the beam, by default 1

        Returns
        -------
        rayleigh_length : float
            The Rayleigh length in mm

        """

        return (np.pi * (waistRadius**2)) / wavelength 

    @staticmethod
    def beam_waist_radius(diamAtLens: float, focalLength: float, wavelength: float, M2: float = 1) -> float:
        """Calculates the beam waist radius given the following parameters.

        Reference: https://www.lasercalculator.com/laser-spot-size-calculator/

        Parameters
        ----------
        diamAtLens : float
            Diameter of the beam at the lens in millimeter
        focalLength : float
            Focal length of the lens in millimeter
        wavelength : float
            Wavelength of the laser light in nanometer
        M2 : float, optional
            Estimated M^2 of the beam, by default 1

        Returns
        -------
        beam_waist_radius : float
            The radius of the beam waist in micrometer

        """
        
        beam_waist_radius = (2 * M2 * wavelength * focalLength) / (np.pi * diamAtLens) 

        return beam_waist_radius / 1000

    def log(self, msg: str, loglevel: int = logging.INFO):
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
        """

        logging.log(loglevel, msg)
        if loglevel >= logging.DEBUG:
            print(f"{logging.getLevelName(loglevel)}: {msg}")

if __name__ == '__main__':
    with Measurement(devMode = False) as M:
        print("with Measurement() as M")
        import code; code.interact(local=locals())
    

    