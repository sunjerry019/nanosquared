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
    """Wrapper around a 32-bit C#.NET library 'NanoScanLibrary.dll'."""

    def __init__(self, host, port, **kwargs):
        # Load the self compiled 'NanoScanLibrary.dll' shared-library file using pythonnet
        super(NanoscanServer, self).__init__(
            # csharp/NanoScanLibrary/bin/Release/netstandard2.0/NanoScanLibrary.dll
            os.path.join(os.path.dirname(__file__),"csharp","NanoScanLibrary","bin","Release","netstandard2.0",'NanoScanLibrary.dll'), 
            'net', host, port
        )
        self.NS = self.lib.NanoScanLibrary.NanoScan()
        self.NS.InitNs()

    # def __getattr__(self, name):
    #     def send(*args, **kwargs):
    #         return getattr(self.NS, name)(*args, **kwargs)
    #     return send

    def GetNumDevices(self):
        return self.NS.GetNumDevices()
    
    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        self.NS.ShutdownNS()
        return super().__exit__(e_type, e_val, traceback)
    
