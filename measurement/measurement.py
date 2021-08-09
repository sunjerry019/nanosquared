#!/usr/bin/env python3

"""File provides the backend for the GUI. It is meant to combine all the modules together"""

from fitting.fitter import ODRFitter
import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

from cameras.camera  import Camera
from cameras.wincamd import WinCamD

from stage.controller import Controller, GSC01

from fitting.fitter import MsqFitter

class Measurement():
    def __init__(self, 
        camera: Camera     = WinCamD, 
        stage : Controller = GSC01   ) -> None:
        
        self.fitter = MsqFitter()

    