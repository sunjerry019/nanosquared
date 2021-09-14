#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys
import numpy as np

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

from cameras.wincamd import WinCamD
from cameras.camera  import Camera
import common.helpers as h

class A(h.LoggerMixIn):
    def __init__(self) -> None:
        self.cam = WinCamD(devMode = False)
        assert isinstance(self.cam, Camera), f"Camera ({self.cam}) is not recognized"

x = A()