#!/usr/bin/env python3

"""File provides the backend for the GUI. It is meant to combine all the modules together"""

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

from cameras.camera  import Camera
from cameras.wincamd import WinCamD

from stage.controller import Controller, GSC01

from fitting.fitter import MsqFitter, MsqOCFFitter

import numpy as np

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

        if controller is None:
            controller = GSC01(devMode = devMode)
        
        if camera is None:
            camera = WinCamD(devMode = devMode)
        
        assert isinstance(camera, Camera), f"Camera ({camera}) is not recognized"
        assert isinstance(controller, Controller), f"Controller ({controller}) is not recognized"

        self.controller = controller
        self.camera     = camera

    def take_measurements(self, rayleighLength: float = 15):
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
        """

        # Check if the rayleigh length fits the stage being used. 

        pass

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




        



if __name__ == '__main__':
    with Measurement() as M:
        print("with Measurement() as M")
        import code; code.interact(local=locals())
    

    