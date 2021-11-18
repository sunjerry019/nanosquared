#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

from msl.loadlib import Server32

import ctypes

class NanoscanServer(Server32):
    """Wrapper around a 32-bit C++ library 'NS2_Interop.dll'."""

    def __init__(self, host, port, **kwargs):
        # Load the 'my_lib' shared-library file using ctypes.CDLL
        
        # https://readthedocs.org/projects/msl-loadlib/downloads/pdf/latest/
        # We know that the DLL uses __cdecl calling type -> ctypes
        super(NanoscanServer, self).__init__(os.path.join(os.path.dirname(__file__),'NS2_Interop.dll'), 'cdll', host, port)
    
    def InitNsInterop(self):
        return self.lib.InitNsInterop()

    def NsInteropGetNumDevices(self):
        x = ctypes.c_short(-1)
        self.lib.NsInteropGetNumDevices(ctypes.byref(x))
        return x

    def setShowWindow(self, showGUI):
        return self.lib.NsInteropSetShowWindow()