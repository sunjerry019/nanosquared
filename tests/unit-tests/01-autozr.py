#!/usr/bin/env python3

import os, sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "../../src/", "nanosquared"))
sys.path.insert(0, root_dir)

from measurement.measure import Measurement
import measurement.errors as me

from cameras.nanoscan import NanoScan
from stage.controller import GSC01

from fitting.fit_functions import omega_z

import logging

import numpy as np

# https://stackoverflow.com/a/287944/3211506
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def test_print(num, message):
    print(f"{bcolors.HEADER}=======>{bcolors.ENDC} [{bcolors.HEADER}Test {num}{bcolors.ENDC}]: {message}")

n = NanoScan(devMode = True)
c = GSC01(devMode = True)

#### TEST 1: z_R OUT OF RANGE
class OutOfRange_Measurement(Measurement):
    LOGLEVEL_THRESHOLD = logging.ERROR

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    SIMULATION_PARAMS = {
        "z_R"   : 107.0873322, # mm
        "w_0"   : 280        , # um
        "z_0"   : 0          , # mm
        "lambda": 2300         # nm
    }
    def simulate_beam(self, pos: int):
        """Simulates a beam with:
            z_0 = 0 mm, w_0 = 280 um, lambda = 2300 nm
            z_R = 107.0873 mm = 107087 um

        Parameters
        ----------
        pos : int
            Position

        Returns
        -------
        d4sigma : Tuple[float, float]
            d4Sigma diameter obtained in the form: [diam, delta diam]
        """
        
        # z in mm
        return [2 * omega_z(z = self.controller.pulse_to_um(pos) / 1000, params = [280,0,2300]), 10]

with OutOfRange_Measurement(devMode = True, camera = n, controller = c) as M:
    test_print(1, "z_R out of range (Single-Axis)...")
    try:
        center = M.find_center(axis = M.camera.AXES.X)
        z_R    = M.find_zR_pps(axis = M.camera.AXES.X, center = center, precision = 100)
        test_print(1, f"z_R out of range (Single-Axis)...[{bcolors.FAIL}FAIL{bcolors.ENDC}]")
    except me.StageOutOfRangeError as e:
        test_print(1, f"z_R out of range (Single-Axis)...[{bcolors.OKGREEN}OK{bcolors.ENDC}]")

    test_print(2, "z_R out of range (Both-Axis)...")
    try:
        center = M.find_center(axis = M.camera.AXES.BOTH)
        print(center)
        z_R    = M.find_zR_pps(axis = M.camera.AXES.BOTH, center = center, precision = 100)
        test_print(2, f"z_R out of range (Both-Axis)...[{bcolors.FAIL}FAIL{bcolors.ENDC}]")
    except me.StageOutOfRangeError as e:
        test_print(2, f"z_R out of range (Both-Axis)...[{bcolors.OKGREEN}OK{bcolors.ENDC}]")

class Asym_Measurement(Measurement):
    # LOGLEVEL_THRESHOLD = logging.ERROR
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    SIMULATION_PARAMS = {
        "z_R"   : 107.0873322, # mm
        "w_0"   : 280        , # um
        "z_0"   : 50         , # mm
        "lambda": 2300         # nm
    }
    def simulate_beam(self, pos: int):
        """Simulates a beam with:
            z_0 = 0 mm, w_0 = 280 um, lambda = 2300 nm
            z_R = 107.0873 mm = 107087 um

        Parameters
        ----------
        pos : int
            Position

        Returns
        -------
        d4sigma : Tuple[float, float]
            d4Sigma diameter obtained in the form: [diam, delta diam]
        """
        
        # z in mm
        return [2 * omega_z(z = self.controller.pulse_to_um(pos) / 1000, params = [280,50,2300]), 10]

with Asym_Measurement(devMode = True, camera = n, controller = c) as M:
    referenceVal = M.controller.um_to_pulse(um = M.SIMULATION_PARAMS['z_R'] * 1000, asint = True )

    test_print(3, "z_R Asymmetric (Single-Axis)...")
    try:
        center = M.find_center(axis = M.camera.AXES.X)
        z_R    = M.find_zR_pps(axis = M.camera.AXES.X, center = center, precision = 100, kappa1 = 0.1)
        print(f"z_R = {z_R}")
        assert np.isclose(a = z_R, b = referenceVal, atol = 100, rtol = 0)
        test_print(3, f"z_R Asymmetric (Single-Axis)...[{bcolors.OKGREEN}OK{bcolors.ENDC}]")
    except Exception as e:
        test_print(3, f"z_R Asymmetric (Single-Axis)...[{bcolors.FAIL}FAIL{bcolors.ENDC}]")
        

    test_print(4, "z_R Asymmetric (Both-Axis)...")
    try:
        center = M.find_center(axis = M.camera.AXES.BOTH)
        print(center)
        z_R    = M.find_zR_pps(axis = M.camera.AXES.BOTH, center = center, precision = 100, kappa1 = 0.1)
        print(f"z_R = {z_R}")
        assert np.allclose(a = z_R, b = [referenceVal, referenceVal], atol = 100, rtol = 0)
        test_print(4, f"z_R Asymmetric (Both-Axis)...[{bcolors.OKGREEN}OK{bcolors.ENDC}]")
    except Exception as e:
        test_print(4, f"z_R Asymmetric (Both-Axis)...[{bcolors.FAIL}FAIL{bcolors.ENDC}]")

