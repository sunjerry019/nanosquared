#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam

import logging
import time

from msl.loadlib import Client64
from nanoscan_constants import SelectParameters as NsSP

class NanoScan(cam.Camera):
	"""Provides interface to the NanoScan 2s Pyro/9/5"""

	def __init__(self, devMode: bool = False, *args, **kwargs):
		cam.Camera.__init__(self, *args, **kwargs)

		self.devMode = devMode
		self.NS = NanoScanDLL() # Init and Shutdown is done by the 32-bit server

		assert self.NS.GetNumDevices() > 0, "No devices connected"

		self.daqState = False
		self.aperture = 0
		self.roiIndex = 0
	
	def SetDAQ(self, state: bool) -> None:
		"""Sets the DAQ state. Use this instead of directly using `self.NS.SetDataAcquisition`. This helps to keep track of the DAQ State.

		Parameters
		----------
		state : bool
			Sets the Data Acquisition to `state`

		"""

		self.NS.SetDataAcquisition(state)
		self.daqState = state

	def start(self) -> int:
		# self.NS.SetShowWindow(True)
		self.SetDAQ(True)
		self.waitForData()
		self.NS.SelectParameters(NsSP.BEAM_WIDTH_D4SIGMA)
		x = self.NS.GetBeamWidth4Sigma(self.aperture, self.roiIndex)
		self.SetDAQ(False)
		return x
	
	def waitForData(self) -> bool:
		"""A valid method of determining whether data has been processed yet is
		to evaluate whether any Results (Parameters per NS1) have yet been computed.
		In this example the Centroid position result is used due to its benign
		nature, i.e. usually enabled and not affected by other settings or results.

		Reference: Program.cs from Automation examples folder from NanoScan
		"""
		if not self.daqState:
			self.log("Start DAQ before waiting for data. Ignoring function call", logging.WARN)
			return False

		self.NS.SelectParameters(
			NsSP.BEAM_CENTROID_POS
		)

		daqState = False
		centroidValue = 0
		while not daqState:
			time.sleep(50e-3)
			centroidValue = self.NS.GetCentroidPosition(self.aperture, self.roiIndex)

			if (centroidValue > 0):
				daqState = True
		
		return True

	def __exit__(self, e_type, e_val, traceback):
		self.NS.__exit__(e_type, e_val, traceback)
		return super(NanoScan, self).__exit__(e_type, e_val, traceback)

class NanoScanDLL(Client64):
	"""Provides interface to the 32-bit NanoScan C# DLL using msl-loadlib."""

	def __init__(self, *args, **kwargs):
		Client64.__init__(self, module32='nanoscan_server.py')

	def __getattr__(self, name):
		def send(*args, **kwargs):
			return self.request32(name, *args, **kwargs)
		return send

	def __enter__(self):
		return self

	def __exit__(self, e_type, e_val, traceback):
		return self.ShutdownNS()
		# return super().__exit__(e_type, e_val, traceback)

if __name__ == '__main__':
    with NanoScan() as n:
        print("with Nanoscan as n")
        import code; code.interact(local=locals())