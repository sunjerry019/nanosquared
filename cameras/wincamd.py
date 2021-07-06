#!/usr/bin/env python3

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam

import logging
from PyQt5 import QtWidgets, QAxContainer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class WinCamD(cam.Camera):
	def __init__(self, *args, **kwargs):
		self.dummyapp = QtWidgets.QApplication([''])
		self.dataCtrl = QAxContainer.QAxWidget("DATARAYOCX.GetDataCtrl.1")
				
		assert self.dataCtrl.dynamicCall("StartDriver") # Returns True if successful

		super().__init__(*args, **kwargs)

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
		if ret:
			self.apertureOpen = False
		
		return ret
	
	def __exit__(self, e_type, e_val, traceback):
		if self.deviceOn:
			self.stopDevice()

		return super().__exit__(e_type, e_val, traceback)

if __name__ == '__main__':
    with WinCamD() as w:
        print("with WinCamD as w")
        import code; code.interact(local=locals())