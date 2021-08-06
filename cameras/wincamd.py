#!/usr/bin/env python3

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam
from cameras.constants import WCD_Profiles, OCX_Buttons, CLIP_MODES

import logging
from PyQt5 import QtWidgets, QAxContainer
from PyQt5 import QtCore

import queue
import asyncio

import numpy as np
from collections import namedtuple

import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class WinCamD(cam.Camera):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.dummyapp = QtWidgets.QApplication([''])
		self.dataCtrl = QAxContainer.QAxWidget("DATARAYOCX.GetDataCtrl.1")
				
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
		assert self.dataCtrl.dynamicCall(f"SetClipLevel(0, 0.5, {CLIP_MODES.D4SIGMA_METHOD}, {CLIP_MODES.CLIP_LEVEL_METHOD})")

		self.dataReadyCallbacks = queue.Queue() # Queue of callbacks to run when data ready

		# https://stackoverflow.com/questions/36442631/how-to-receive-activex-events-in-pyqt5
		self.dataCtrl.DataReady.connect(self.on_DataReady)

	def on_DataReady(self):
		"""When the DataReady event is fired, run dataReady callbacks
		"""
		
		callbacks = []
		
		while True:
			try:
				fun = self.dataReadyCallbacks.get(block = False)
				print(f"DataReady task {fun}")
				callbacks.append(fun)
				# Pop all at once and then run later so that
				# Functions can add callbacks to the dataReady stack
				# to be called in the next cycle
			except queue.Empty as e:
				print("End of queue")
				break

		for fun in callbacks:
			fun()
			print(f"DataReady task {fun} done")
			self.dataReadyCallbacks.task_done()
			# Since it was FIFO, it should not matter that we do this later
		
		print("End of one RTT\n")
	
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

	def d4sig(self):
		self.stopDevice()
		print(w.getAxis_D4Sigma('x', direct = True))

	def getAxis_D4Sigma(self, axis):
		"""Get the d4sigma in one `axis`, opens the camera if necessary.

		The function closes the camera before obtaining the data, then restores the previous state that the camera was in.

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
		if self.originalState is None:
			self.originalState = self.apertureOpen

		if not self.apertureOpen:
			assert self.startDevice()

		d4Sigma = {
			"x"  : self.dataCtrl.dynamicCall(f"GetOCXResult({OCX_Buttons.u_WinCamD_Width_at_Clip_1})"),
			"y"  : self.dataCtrl.dynamicCall(f"GetOCXResult({OCX_Buttons.v_WinCamD_Width_at_Clip_1})")
		}

		self.D4Sigma_data = None

		def temp_func():
			self.stopDevice()
			self.D4Sigma_data = d4Sigma.get(axis, None)
			if self.originalState:
				self.startDevice()

		self.dataReadyCallbacks.put(temp_func)
		self.wait_DataReady_Tasks()

		return self.D4Sigma_data

	def getAxisProfile(self, axis):
		"""Get the profile in one `axis` if the camera is running.

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