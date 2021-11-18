#!/usr/bin/env python3

"""Provides enums for NanoScan"""

from enum import IntFlag, IntEnum, auto

class NsAxes(IntEnum):
    """Enum for Axis Selection"""
    X = auto()
    Y = auto()

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


