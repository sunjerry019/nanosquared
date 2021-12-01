#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam
from cameras.nanoscan_constants import SelectParameters, NsAxes

import logging

from PyQt5 import QtWidgets, QAxContainer, QtCore

from typing import Tuple

class NanoScan(cam.Camera):
    """Provides interface to the NanoScan 2s Pyro/9/5"""

    def __init__(self, devMode: bool = False, *args, **kwargs):
        cam.Camera.__init__(self, *args, **kwargs)
        self.apertureOpen = False

        self.devMode = devMode

        self.dummyapp = QtWidgets.QApplication([''])

        # Early Binding: NanoScanII.INanoScanII
        # We have to use Late Binding
        # QAxObject for COM object vs. QAxWidget
        self.NS = QAxContainer.QAxObject("photon-nanoscan")  # {FAAD0D22-C718-459A-81CA-268CCF188807}\

    def getAxis_avg_D4Sigma(self, axis, numsamples: int = 20) -> Tuple[float, float]:
        """Get the d4sigma in one `axis` and averages it over `numsamples`.
		This function opens the camera where necessary, and returns it to the previous state after it is done.

		Parameters
		----------
		axis : str
			May take values 'x' or 'y'
		numsamples : int, optional
			Number of samples to average over, by default 20

		Returns
		-------
		ret : (double, double)
			Returns the d4sigma of the given axis in micrometer in the form of (average, stddev)
			If the given `axis` is not 'x' or 'y', then (`None`, `None`)
			
		"""
        # self.NS.dynamicCall("NsAsAutoFind()")
        # self.NS.dynamicCall("NsAsSelectParameters(long)", 
        #     SelectParameters.BEAM_WIDTH_D4SIGMA & SelectParameters.BEAM_CENTROID_POS)

        # # Take sample
        # self.NS.dynamicCall("NsAsAcquireSync1Rev()")
        # self.NS.dynamicCall("NsAsRunComputation()")
        # # NsAsRecompute() for no tracking performed even if setup 'sync1rev

        # # Axis, ROI Index, *Beam Width
        # x = [-0.1]
        # y = [-0.1]

        # self.NS.dynamicCall("NsAsGetBeamWidth4Sigma(short, short, float&)", NsAxes.X, 0, x)
        # self.NS.dynamicCall("NsAsGetBeamWidth4Sigma(short, short, float&)", NsAxes.Y, 0, y)
        # self.log((x, y), loglevel = logging.INFO)

        self.NS.dynamicCall("NsAsDataAcquisition", True)

        x = [-0.1]
        y = [-0.1]

        self.NS.dynamicCall("NsAsGetBeamWidth(short, short, float, float&)", 0, 0, 13.5, x)
        self.NS.dynamicCall("NsAsGetBeamWidth(short, short, float, float&)", 1, 0, 13.5, y)
        
        self.NS.dynamicCall("NsAsDataAcquisition", False)

        return (x[0], y[0])

    def toggleWindow(self) -> None:
        """Toggles the GUI Window of the NanoScan program"""

        state = self.NS.dynamicCall("NsAsShowWindow")
        self.NS.dynamicCall("NsAsShowWindow", not state)

    def getNumDevices(self) -> int:
        """Gets the number of connected NanoScan devices

        Returns
        -------
        numDevices: int
            Number of NanoScan devices connected.
        """
        numDevices = [-1] # Forces pass-by-reference
        x = self.NS.dynamicCall("NsAsGetNumDevices(short&)", numDevices) # https://stackoverflow.com/a/25378588
        return numDevices[0]
    
    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        pass

if __name__ == '__main__':
    with NanoScan() as n:
        print("with Nanoscan as n")
        import code; code.interact(local=locals())