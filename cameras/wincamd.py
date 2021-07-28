#!/usr/bin/env python3

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam
from cameras.constants import WCD_Profiles

import logging
from PyQt5 import QtWidgets, QAxContainer
from PyQt5 import QtCore

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

		self.axis.x.show()
		self.axis.y.show()

		# # https://www.tutorialspoint.com/pyqt/pyqt_signals_and_slots.htm
		# QtCore.connect(self.dataCtrl, QtCore.pyqtSignal('DataReady()'), self.on_DataReady)

		# # https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html
		# self.DataReady = QtWidgets.QAction("DataReady()". s)

		# time.sleep(1)
		# self.axis.x.setWindowState(QtCore.Qt.WindowMinimized)
		# self.axis.y.setWindowState(QtCore.Qt.WindowMinimized)

		# self.axis.x.hide()
		# self.axis.y.hide()

		# self.axis.x.showMinimized()
		# self.axis.y.showMinimized()

	# https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html#the-pyqtslot-decorator
	# @QtCore.pyqtSlot(str, int, "void *")
	# def slot(self, name, argc, argv):
	# 	print(f"{name}")

	def on_DataReady(self):
		print("DataReady")
		

	def getAxisProfile(self, axis):
		"""Get the profile in one `axis` if the camera is running.

		Parameters
		----------
		axis : str
			May take values 'x' or 'y'.

		Returns
		-------
		ret : Union[array, None]
			If the given `axis` is not 'x' or 'y', then `None`

		"""
		if not self.apertureOpen:
			return None

		data = {
			"x": self.axis.x.dynamicCall("GetProfileDataAsVariant"),
			"y": self.axis.y.dynamicCall("GetProfileDataAsVariant")
		}
		return np.array(data.get(axis, None))
	
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