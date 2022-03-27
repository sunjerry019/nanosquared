#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os

from msl.loadlib import Server32

import clr
import System

class NanoScanServer(Server32):
    """Wrapper around a 32-bit C#.NET library 'NanoScanLibrary.dll'. WARNING: No GUI Features available."""

    def __init__(self, host, port, **kwargs):
        # Load the self compiled 'NanoScanLibrary.dll' shared-library file using pythonnet
        path = Server32.remove_site_packages_64bit()
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

    def GetHeadScanRates(self):
        """Overloads GetHeadScanRates so that we can convert the return values to list.
        
        Otherwise it throws an error as it cannot pickle Single[] objects to send to tbe 64-bit program.
        """

        return list(self.NS.GetHeadScanRates())

    def __getattr__(self, name):
        """Get the functions of self.NS directly. Possibly use python script to generate functions in this file.
        
        See NanoScan.cs for functions and documentations
        """
        def send(*args, **kwargs):
            return getattr(self.NS, name)(*args, **kwargs)
        return send

    def log(self, message):
        with open(os.path.join(os.path.dirname(__file__), "log.log"), 'a') as f:
            f.write(str(message))
            f.write("\n")

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        self.NS.ShutdownNS()
        return super().__exit__(e_type, e_val, traceback)
    
