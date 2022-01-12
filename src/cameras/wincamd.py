#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

from typing import Tuple

import cameras.camera as cam
from cameras.wincamd_constants import WinCamAxes, WCD_Profiles, OCX_Buttons, CLIP_MODES

import logging
from PyQt5 import QtWidgets, QAxContainer
# from PyQt5 import QtCore

import queue

import numpy as np
from collections import namedtuple

class WinCamD(cam.Camera):
	AXES = WinCamAxes
	
	def __init__(self, devMode: bool = False, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.devMode = devMode

		self.dummyapp = QtWidgets.QApplication([''])
		self.dataCtrl = QAxContainer.QAxWidget("DATARAYOCX.GetDataCtrl.1")
		
		if not self.devMode:
			self.log("Not DevMode, starting driver", loglevel=logging.DEBUG)
			assert self.dataCtrl.dynamicCall("StartDriver") # Returns True if successful

		axis = {
			"x" : QAxContainer.QAxWidget("DATARAYOCX.ProfilesCtrl.1"),
			"y" : QAxContainer.QAxWidget("DATARAYOCX.ProfilesCtrl.1")
		}
		self.axis = namedtuple("Axis", axis.keys())(*axis.values())

		# For the ProfileID Values, look at dataray-profiles-enum.pdf
		self.axis.x.setProperty("ProfileID", WCD_Profiles.WC_PROFILE_X)
		self.axis.y.setProperty("ProfileID", WCD_Profiles.WC_PROFILE_Y)

		self.axis.x.show() # u
		self.axis.y.show() # v

		self.prof_data = None

		# For getting d4sigma
		self.D4Sigma_data  = None
		self.originalState = None
		# Percentage in decimal notation (A, B, MODE_A, MODE_B)
		# If mode = D4SIGMA, then the clip levels don't matter
		assert self.setClipMode(CLIP_MODES.D4SIGMA_METHOD)

		self.dataReadyCallbacks = queue.Queue() # Queue of callbacks to run when data ready

		# https://stackoverflow.com/questions/36442631/how-to-receive-activex-events-in-pyqt5
		self.dataCtrl.DataReady.connect(self.on_DataReady)

		# Last thing we do is to make sure our camera is warmed up and ready
		# if not self.devMode:
			# self.wait_stable()

	# Support functions
	def on_DataReady(self):
		"""When the DataReady event is fired, run dataReady callbacks
		"""
		
		callbacks = []
		
		while True:
			try:
				fun = self.dataReadyCallbacks.get(block = False)
				self.log(f"DataReady task {fun}", logging.DEBUG)
				callbacks.append(fun)
				# Pop all at once and then run later so that
				# Functions can add callbacks to the dataReady stack
				# to be called in the next cycle
			except queue.Empty as e:
				self.log("End of queue", logging.DEBUG)
				break

		for fun in callbacks:
			fun()
			self.log(f"DataReady task {fun} done", logging.DEBUG)
			self.dataReadyCallbacks.task_done()
			# Since it was FIFO, it should not matter that we do this later
		
		self.log("End of one RTT\n", logging.DEBUG)
	
	def wait_DataReady_Tasks(self):
		"""Waits for all the dataready callbacks to be called
		"""
		# self.dataReadyCallbacks.join()
		while True:
			if self.dataReadyCallbacks.empty():
				break
			else:
				# Hack to force DataReady to process
				# Supposedly not a kosher way of doing this but I really dk
				# how to concurrency
				QtWidgets.QApplication.processEvents()

	def wait_stable(self, numevents: int = 10):
		"""Blocks until `numevents` of DataReady has passed. Opens the camera if necessary, then restores the previous state. 

		Parameters
		----------
		numevents : int, optional
			Number of DataReady events to wait for, by default 10

		"""
		_originalState = self.apertureOpen
		if not self.apertureOpen:
			self.startDevice()

		def temp_func(i):
			if i > 0:
				self.dataReadyCallbacks.put(lambda: temp_func(i - 1))

		self.dataReadyCallbacks.put(lambda: temp_func(numevents - 1))
		self.wait_DataReady_Tasks()

		if not _originalState:
			self.stopDevice()

		return True

	def setClipMode(self, mode, clip: float = 0):
		"""Sets the clip mode for Clip A (i.e. 1). Throughout this code, we will only be using A

		If mode = D4SIGMA, then the clip levels don't matter

		Parameters
		----------
		mode : int
			Can type values 0, or 1:
			0 = CLIP_LEVEL_METHOD
			1 = D4SIGMA_METHOD
		clip : float
			Value between 0 and 1, determines the clip level, if mode is CLIP_LEVEL_METHOD

		Returns
		-------
		ret : bool
			True if success
		"""

		if mode == CLIP_MODES.D4SIGMA_METHOD:
			clip = 0
		elif mode == CLIP_MODES.CLIP_LEVEL_METHOD:
			if not (0 <= clip <= 1):
				self.log(f"Invalid clip level {clip} received", logging.WARN)
				return False
		else:
			return False

		# Percentage in decimal notation (A, B, MODE_A, MODE_B)
		return self.dataCtrl.dynamicCall(f"SetClipLevel({clip}, 0.5, {mode}, {CLIP_MODES.CLIP_LEVEL_METHOD})")

	# Implementations
	def getAxis_avg_D4Sigma(self, axis: WinCamAxes, numsamples: int = 20) -> Tuple[float, float]:
		"""Get the d4sigma in one `axis` and averages it over `numsamples`.
		This function opens the camera where necessary, and returns it to the previous state after it is done.

		IMPT: Ensure that the camera has already corrected the baseline artefact. 
		You can do this by starting the device and waiting for a few DataReady events.
		This is provided the by function `self.wait_stable()`

		Parameters
		----------
		axis : str
			May take values 'x' or 'y'
		numsamples : int, optional
			Number of samples to average over, by default 20

		Returns
		-------
		ret : (float, float)
			Returns the d4sigma of the given axis in micrometer in the form of (average, stddev)
			If the given `axis` is not 'x' or 'y', then (`None`, `None`)
			
		"""

		frames_needed_for_stable = 8  # Empirical Data
		
		if axis not in ['x', 'y']:
			return (None, None)

		if self.devMode:
			return (123, 10)

		# Ensure we are in d4sigma mode:
		mode = self.dataCtrl.dynamicCall(f"GetClipLevelMode(1)")
		if mode != CLIP_MODES.D4SIGMA_METHOD:
			self.setClipMode(CLIP_MODES.D4SIGMA_METHOD)

		_originalState = self.apertureOpen

		if not self.apertureOpen:
			assert self.startDevice()
		
		# We discard the first data point because of some artefact
		data = np.array([self.getAxis_D4Sigma(axis) for _ in range(numsamples + frames_needed_for_stable)][frames_needed_for_stable:])

		if not _originalState:
			self.stopDevice()
		
		self.log(f"Getting average of {len(data)} data points: \n{data}", logging.INFO)

		return (np.average(data), np.std(data))

	def getAxis_D4Sigma(self, axis: WinCamAxes):
		"""Get the d4sigma in one `axis`, opens the camera if necessary, then restores the previous state that the camera was in.

		IMPT: You should discard the data to the first call to the function, then take some averages. 
		This is some artefact where it keeps returning the previous data point. 

		Parameters
		----------
		axis : str
			May take values 'x' or 'y'

		Returns
		-------
		ret : double
			Returns the d4sigma of the given axis in micrometer. 
			If the given `axis` is not 'x' or 'y', then `None`.

		"""
		_originalState = self.apertureOpen

		if not self.apertureOpen:
			assert self.startDevice()

		d4Sigma = {
			"x"  : self.dataCtrl.dynamicCall(f"GetOCXResult({OCX_Buttons.u_WinCamD_Width_at_Clip_1})"),
			"y"  : self.dataCtrl.dynamicCall(f"GetOCXResult({OCX_Buttons.v_WinCamD_Width_at_Clip_1})")
		}

		self.D4Sigma_data = None

		def temp_func():
			self.D4Sigma_data = d4Sigma.get(axis, None)
			if not _originalState:
				self.stopDevice()
			
		self.dataReadyCallbacks.put(temp_func)
		self.wait_DataReady_Tasks()

		return self.D4Sigma_data

	def getAxisProfile(self, axis: WinCamAxes):
		"""Get the profile in one `axis` if the camera is running.
		Note: Does not work, but not important 

		Parameters
		----------
		axis : str
			May take values 'x', 'y', or 'xy'

		Returns
		-------
		ret : Union[array, None]
			If the given `axis` is not 'x', 'y', or 'xy', then `None`

		"""
		if not self.apertureOpen:
			return None

		data = {
			"x"  : np.array(self.axis.x.dynamicCall("GetProfileDataAsVariant")),
			"y"  : np.array(self.axis.y.dynamicCall("GetProfileDataAsVariant"))
		}

		self.prof_data = None

		if axis in data:
			def temp_func():
				self.prof_data = data.get(axis, None)
			self.dataReadyCallbacks.put(temp_func)
		elif axis == 'xy':
			self.prof_data = [0, 0]
			def temp_x():
				self.prof_data[0] = data["x"]
			def temp_y():
				self.prof_data[1] = data["y"]

			self.dataReadyCallbacks.put(temp_x)
			self.dataReadyCallbacks.put(temp_y)
		
		self.wait_DataReady_Tasks()

		return self.prof_data
	
	def getWinCamData(self):
		"""Gets the WinCam Data as a numpy_array if the camera is running, else `None`

		Returns
		-------
		data : Union[array_like, None]
			returns the data, or None if the camera is not running.

		"""
		if not self.apertureOpen:
			return None

		vert = self.dataCtrl.dynamicCall("GetVerticalPixels")
		hori = self.dataCtrl.dynamicCall("GetHorizontalPixels")
		return np.array(self.dataCtrl.dynamicCall("GetWinCamDataAsVariant")).reshape((vert, hori))

	def getCameraIndex(self):
		return self.dataCtrl.dynamicCall("GetCameraIndex")

	# Basic Functions
	def startDevice(self):
		"""Starts the Camera capturing

		Returns
		-------
		ret : bool
			True if the device is successfully started

		"""
		ret = self.dataCtrl.dynamicCall("StartDevice")
		self.apertureOpen = ret
		
		return ret
	
	def stopDevice(self):
		"""Stops the Camera from capturing

		Returns
		-------
		ret : bool
			True if the device is successfully stopped

		"""

		ret = self.dataCtrl.dynamicCall("StopDevice")
		# Seems to always return false
		self.apertureOpen = False
		
		return ret

	def __exit__(self, e_type, e_val, traceback):
		if self.apertureOpen:
			self.stopDevice()

		return super().__exit__(e_type, e_val, traceback)

if __name__ == '__main__':
    with WinCamD() as w:
        print("with WinCamD as w")
        import code; code.interact(local=locals())