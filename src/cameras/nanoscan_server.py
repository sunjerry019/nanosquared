#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

from msl.loadlib import Server32

import clr
import System

class NanoScanServer(Server32):
    """Wrapper around a 32-bit C#.NET library 'NanoScanLibrary.dll'. WARNING: No GUI Features available."""

    def __init__(self, host, port, **kwargs):
        # Load the self compiled 'NanoScanLibrary.dll' shared-library file using pythonnet
        try:
            super(NanoScanServer, self).__init__(
                # csharp/NanoScanLibrary/bin/Release/netstandard2.0/NanoScanLibrary.dll
                os.path.join(os.path.dirname(__file__),"csharp","NanoScanLibrary","bin","Release","netstandard2.0",'NanoScanLibrary.dll'), 
                'net', host, port
            )
        except System.NotSupportedException as e:
            # Likely LoadFromRemoteSources error
            super(NanoScanServer, self).__init__(
                # csharp/NanoScanLibrary/bin/Release/netstandard2.0/NanoScanLibrary.dll
                os.path.join("C:/", "nanosquared_include", 'NanoScanLibrary.dll'), 
                'net', host, port
            )

        self.NS = self.lib.NanoScanLibrary.NanoScan()
        assert self.NS.InitNS() == 1, "Failed to start NanoScan"

    def __getattr__(self, name):
        """Get the functions of self.NS directly. Possibly use python script to generate functions in this file.
        
        See NanoScan.cs for functions and documentations
        """
        def send(*args, **kwargs):
            return getattr(self.NS, name)(*args, **kwargs)
        return send

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        self.NS.ShutdownNS()
        return super().__exit__(e_type, e_val, traceback)
    
