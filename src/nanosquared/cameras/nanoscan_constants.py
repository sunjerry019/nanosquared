#!/usr/bin/env python3

"""Provides enums for NanoScan"""

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir) 

from enum import IntFlag, IntEnum, auto

from cameras.all_constants import CameraAxes

class NsAxes(CameraAxes, IntEnum):
    """Enum for Axis Selection"""
    X    = 0
    Y    = 1
    BOTH = 2

class BeamWidthBasis(IntEnum):
    """Enum for NsAsBeamWidthBasis"""
    W_13_5    = auto()
    W_50      = auto()
    W_D4SIGMA = auto()
    W_USER_1  = auto()
    W_USER_2  = auto()

class SelectParameters(IntFlag):
    """Enum for NsAsSelectParameters"""
    BEAM_WIDTH_13_5_CLIP         = auto()
    BEAM_WIDTH_FWHM_CLIP         = auto()
    BEAM_WIDTH_USER_CLIP_1       = auto()
    BEAM_WIDTH_USER_CLIP_2       = auto()
    BEAM_WIDTH_D4SIGMA           = auto()
    BEAM_CENTROID_POS            = auto()
    BEAM_PEAK_POS                = auto()
    SEP_CENTROID                 = auto()
    SEP_PEAK                     = auto()
    BEAM_PEAK                    = auto()
    PROFILE_GAUSS_FIT            = auto()
    ELLIPTICITY                  = auto()
    POWER                        = auto()
    POWER_TOTAL                  = auto()
    DIVERGENCE                   = auto()
    BEAM_WIDTH_RATIO_13_5_CLIP   = auto()
    BEAM_WIDTH_RATIO_FWHM_CLIP   = auto()
    BEAM_WIDTH_RATIO_USER_CLIP_1 = auto()
    BEAM_WIDTH_RATIO_USER_CLIP_2 = auto()
    BEAM_WIDTH_RATIO_D4SIGMA     = auto()


