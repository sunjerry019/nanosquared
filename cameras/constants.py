#!/usr/bin/env python3

"""
Provides reference lookup for WinCamD. 
"""

from collections import namedtuple


# For the ProfileID Values, look at dataray-profiles-enum.pdf
_profiles = [
    "DEFAULT_PROFILE" ,
    "BS_PROFILE_X" ,
    "BS_PROFILE_Y" ,
    "BS_PROFILE_S" ,
    "BR_PROFILE_X" ,
    "BR_PROFILE_Y" ,
    "BM_PROFILE_ZM2" ,
    "BM_PROFILE_ZM1" ,
    "BM_PROFILE_Z" ,
    "BM_PROFILE_ZP1" ,
    "BM_PROFILE_ZP2" ,
    "BM_PROFILE_M45" ,
    "BM_PROFILE_P45" ,
    "BM_PROFILE_Z2" ,
    "BC_PROFILE_U1" ,
    "BC_PROFILE_V1" ,
    "BC_PROFILE_U2" ,
    "BC_PROFILE_V2" ,
    "BC_PROFILE_U3" ,
    "BC_PROFILE_V3" ,
    "BC_PROFILE_U4" ,
    "BC_PROFILE_V4" ,
    "WC_PROFILE_X" ,
    "WC_PROFILE_Y" ,
    "WC_PROFILE_XB" ,
    "WC_PROFILE_YB" ,
    "WC_DIV_X" ,
    "WC_DIV_Y" ,
]

WCD_Profiles = namedtuple("Profiles", _profiles)(*range(len(_profiles)))