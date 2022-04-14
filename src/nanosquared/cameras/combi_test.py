#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys
import numpy as np

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir) 

from cameras.wincamd import WinCamD
from cameras.nanoscan import NanoScan
from cameras.camera  import Camera
import common.helpers as h

from stage.controller import Controller, GSC01

class A(h.LoggerMixIn):
    def __init__(self) -> None:
        self.controller = GSC01(devMode = False)
        self.cam = NanoScan(devMode = False)
        assert isinstance(self.cam, Camera), f"Camera ({self.cam}) is not recognized"
        print(self.cam.getAxis_avg_D4Sigma(self.cam.AXES.X))

x = A()