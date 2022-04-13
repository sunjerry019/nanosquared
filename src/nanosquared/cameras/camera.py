#!/usr/bin/env python3

"""File provides the class camera that all camera types should inherit"""

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import common.helpers as h

from cameras.all_constants import CameraAxes

class Camera(h.LoggerMixIn):
    AXES = CameraAxes
    def __init__(self):
        self.apertureOpen = False

    def getAxis_avg_D4Sigma(self, axis: CameraAxes, numsamples: int = 20, *args, **kwargs):
        raise NotImplementedError

    def wait_stable(self):
        raise NotImplementedError
    
    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        pass