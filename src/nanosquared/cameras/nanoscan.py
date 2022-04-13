#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import numbers
import os,sys
from typing import Tuple, List

import scipy.signal

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam

import logging
import time

import numpy as np

from msl.loadlib import Client64
from cameras.nanoscan_constants import SelectParameters as NsSP
from cameras.nanoscan_constants import NsAxes

class NanoScan(cam.Camera):
	"""Provides interface to the NanoScan 2s Pyro/9/5. Naive implementation
	   following the example codes. 
	"""
	
	AXES = NsAxes

	def __init__(self, devMode: bool = False, *args, **kwargs):
		cam.Camera.__init__(self, *args, **kwargs)

		self.log("Initializing NanoScan...", end="\r")

		self.devMode = devMode
		if self.devMode:
			self.log("devmode nanoscan: no NanoScanDLL will be available", logging.WARN)
			self.NS = None
		else:
			self.NS = NanoScanDLL() # Init and Shutdown is done by the 32-bit server

		if not self.devMode:
			assert self.NS.GetNumDevices() > 0, "No devices connected"
			assert self.NS.GetDeviceID() > -1, "All devices in use"

		self.daqState = False
		self.roiIndex = 0

		if not self.devMode:
			self._rotFreq = self.NS.GetRotationFrequency()
			self.allowedRots = self.NS.GetHeadScanRates()
		else:
			self._rotFreq    = 10.0
			self.allowedRots = [1.25, 2.5, 5.0, 10.0, 20.0]
		
		self.log("Initializing NanoScan...Done")

	@property
	def rotationFrequency(self):
		return self._rotFreq
	
	@rotationFrequency.setter
	def rotationFrequency(self, freq):
		"""Setter for scan head rotation speed in Hz

		Parameters
		----------
		freq : float
			May take any value from all allowed rotation rates. 
			Use `list(self.NS.GetHeadScanRates())` to obtain available allowed rotation rates. 
		"""
		# Check if the freq is allowed
		if freq not in self.allowedRots:
			self.log(f"Ignoring scan freq {freq} Hz (expected {self.allowedRots})", logging.WARN)
			return

		if not self.devMode:
			# Set the freq
			self.NS.SetRotationFrequency(freq) 
			# GetMaxSamplingResolution and set it as such
			self.NS.SetSamplingResolution(self.NS.GetMaxSamplingResolution())

		self._rotFreq = freq

	@staticmethod
	def remove_spikes(arr: np.ndarray, threshold: float) -> np.ndarray:
		"""Method to remove positive peaks from data.

		Parameters
		----------
		arr : np.ndarray
			Array to remove spikes from
		threshold : float
			Prominence as defined in scipy.signal

		Returns
		-------
		np.ndarray
			result without spikes
		"""
		i = 0
		
		arr_rem = arr
		while True:
			# find peaks
			peaks, _ = scipy.signal.find_peaks(arr_rem, prominence = threshold)

			if len(peaks) == 0:
				break

			# Generate masks
			l    = len(arr_rem)
			mask = np.ones(l, dtype=bool)
			mask[peaks] = False
			arr_rem     = arr_rem[mask]
			
			i += 1

		# manually check first and last points
		l    = len(arr_rem)
		mask = np.ones(l, dtype=bool)

		d = arr_rem[0] - arr_rem[1]
		if np.abs(d) > threshold:
			mask[0] = False

		d = arr_rem[-1] - arr_rem[-2]
		if np.abs(d) > threshold:
			mask[-1] = False

		arr_rem = arr_rem[mask]

		return arr_rem

	def getAxis_avg_D4Sigma(self, axis: NsAxes, numsamples: int = 20, removeOutliers: int = 0, threshold: float = 0.2, *args, **kwargs) -> Tuple[float, float]:
		"""Get the d4sigma in one `axis` and averages it over `numsamples` using the Sync1Rev implementation.

		Using NsAxes somewhat changes the signature of this function in a strict sense, but at this point I think would make easier for me to check.

		Parameters
		----------
		axis : NsAxes
			Either `NsAxes.X` or `NsAxes.Y`, or `NsAxes.BOTH`.
			
			Arguably using `NsAxes.BOTH` is more efficient but leads to 
			spaghetti code in that the return type is no longer consistent.

			This is a compromise I am willing to take. 
		numsamples : int, optional
			Number of samples to average over, by default 20
		removeOutliers: int, optional
			NanoScan has the tendency to output data with high variation. This setting can help to reduce the standard deviation of the results obtained by removing outliers.

			0 = Do not remove outliers, calculate as is
			1 = Remove highest 10% of results
			2 = Remove positive peaks from result based on a threshold of 20% * Mean.

			By default, 0
		threshold: float, optional
			Threshold of peak prominence, must be more than 0. Ignored if `removeOutliers` is not 2.

			If value is less than or equal to 1, then it represents the precentage of the mean to use as the prominence threshold.
			If value is more than 1, then it represents the absolute prominence threshold.

			If an invalid value is given, then threshold = 0.2

			By default 0.2 = 20% of the average.

		Returns
		-------
		ret : (float, float) or array_like of form [[float, float], [float, float]]
			Returns the d4sigma of the given axis in micrometer in the form of (average, stddev) or (x, y) where each axis is given in the form of (average, stddev)
			If the given `axis` is not `NsAxes.X` or `NsAxes.Y` or `NsAxes.XY`, then (`None`, `None`)
		"""
		ret = (None, None)

		if not isinstance(axis, NsAxes):
			self.log(f"Invalid axis {axis} selected, expected axis of type {NsAxes}.")
			return ret

		if removeOutliers not in [0, 1, 2]:
			self.log(f"Invalid removeOutlier mode {removeOutliers}! Using mode 0: do nothing", loglevel = logging.warn)
			removeOutliers = 0 

		if removeOutliers == 2:
			# Check if the threshold is valid:
			if not isinstance(threshold, numbers.Number) or threshold <= 0:
				self.log(f"Invalid threshold {threshold}. Using 0.2.", loglevel = logging.warn)
				threshold = 0.2

		if self.devMode:
			if axis == NsAxes.BOTH:
				ret = np.array([[500,10], [600,25]])
			else:
				ret = (550, 15) 

			return ret

		self.wait_stable()

		self.NS.AutoFind()

		originalParams = self.NS.GetSelectedParameters()
		self.NS.SelectParameters(originalParams | NsSP.BEAM_WIDTH_D4SIGMA)

		# A stack of x, y values
		out = np.array([list(self.oneRev()) for _ in range(numsamples + 10)])

		# Throwaway the first 10 values
		out = out[10:]

		# Remove Outliers
		if removeOutliers == 1:
			# Throw away top 10% of values
			throwout = int(np.around(0.1 * numsamples))
			if axis == NsAxes.BOTH:
				x_axis, y_axis = out[:,0], out[:,1]
				x_axis, y_axis = np.sort(x_axis)[:-throwout], np.sort(y_axis)[:-throwout]

				out = np.column_stack((x_axis, y_axis))
			else:
				out = np.sort(out)[:-throwout]

		if removeOutliers == 2:
			# Remove spike using 20% as the threshold
			if axis == NsAxes.BOTH:
				x_axis, y_axis = out[:,0], out[:,1]
				if threshold <= 1:
					x_axis, y_axis = NanoScan.remove_spikes(x_axis, threshold * np.average(x_axis)), NanoScan.remove_spikes(y_axis, threshold * np.average(y_axis))
				else:
					x_axis, y_axis = NanoScan.remove_spikes(x_axis, threshold), NanoScan.remove_spikes(y_axis, threshold)

				out = np.column_stack((x_axis, y_axis))
			else:
				if threshold <= 1:
					out = NanoScan.remove_spikes(out, threshold * np.average(out))
				else:
					out = NanoScan.remove_spikes(out, threshold)

		average = np.average(out, axis = 0)
		stddev  = np.std(out, axis = 0)

		self.log(f"average = {average}, stddev = {stddev}", loglevel = logging.DEBUG)

		if axis == NsAxes.BOTH:
			ret = np.vstack((average, stddev)).T
		else:
			ret = (average.flatten()[axis], stddev.flatten()[axis])

		self.NS.SelectParameters(originalParams)

		return ret
		
	def oneRev(self) -> Tuple[float, float]:
		self.NS.AcquireSync1Rev()
		self.NS.RunComputation()
		x = self.NS.GetBeamWidth4Sigma(NsAxes.X, self.roiIndex)
		y = self.NS.GetBeamWidth4Sigma(NsAxes.Y, self.roiIndex)

		self.log(f"Got 1 Reading of (x, y): {(x, y)}", logging.DEBUG)

		return (x, y)

	def wait_stable(self) -> bool:
		if self.devMode:
			return True

		self.SetDAQ(True)
		self.waitForData()
		self.SetDAQ(False)
		return True
	
	def SetDAQ(self, state: bool) -> None:
		"""Sets the DAQ state. Use this instead of directly using `self.NS.SetDataAcquisition`. This helps to keep track of the DAQ State.

		Do not use in conjunction with Sync1Rev, it will be useless.

		Parameters
		----------
		state : bool
			Sets the Data Acquisition to `state`

		"""

		if not self.devMode:
			self.NS.SetDataAcquisition(state)

		self.daqState = state
	
	def waitForData(self) -> bool:
		"""A valid method of determining whether data has been processed yet is
		to evaluate whether any Results (Parameters per NS1) have yet been computed.
		In this example the Centroid position result is used due to its benign
		nature, i.e. usually enabled and not affected by other settings or results.

		Reference: Program.cs from Automation examples folder from NanoScan

		Returns
		-------
		success : bool
			Returns true when data is available

		"""

		if not self.daqState:
			self.log("Start DAQ before waiting for data. Ignoring function call", logging.WARN)
			return False

		if self.devMode:
			return True

		originalParams = self.NS.GetSelectedParameters()

		self.NS.SelectParameters(
			originalParams | NsSP.BEAM_CENTROID_POS
		)

		daqState = False
		centroidValue_X = 0
		centroidValue_Y = 0
		cnt = 0

		while not daqState:
			time.sleep(50e-3)
			centroidValue_X = self.NS.GetCentroidPosition(NsAxes.X, self.roiIndex)
			centroidValue_Y = self.NS.GetCentroidPosition(NsAxes.Y, self.roiIndex)

			self.log(f"{cnt}: waitStable: Centroid ({centroidValue_X}, {centroidValue_Y})", logging.DEBUG, end = "\r")

			cnt += 1

			if (centroidValue_X > 0) and (centroidValue_Y > 0):
				daqState = True

		self.NS.SelectParameters(originalParams)
		
		return True

		# def freeRunning(self, axis: NsAxes = NsAxes.X) -> float:
		# 	# self.NS.SetShowWindow(True)
		# 	self.SetDAQ(True)
		# 	self.waitForData()
		# 	self.NS.SelectParameters(NsSP.BEAM_WIDTH_D4SIGMA)
		# 	x = self.NS.GetBeamWidth4Sigma(axis, self.roiIndex)
		# 	self.SetDAQ(False)
		# 	return x

	def __exit__(self, e_type, e_val, traceback):
		if not self.devMode:
			self.NS.__exit__(e_type, e_val, traceback)
		return super(NanoScan, self).__exit__(e_type, e_val, traceback)

class NanoScanDLL(Client64):
	"""Provides interface to the 32-bit NanoScan C# DLL using msl-loadlib."""

	def __init__(self, *args, **kwargs):
		serv32 = os.path.join(os.path.dirname(__file__), 'nanoscan_server.py')
		Client64.__init__(self, module32 = serv32)

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