#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys

import ctypes

import win32com

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam

import logging
from PyQt5 import QtWidgets, QAxContainer, QtCore

import numpy as np
from collections import namedtuple

# import nanoscan_activex as NSAx
import win32com.client as wc

class NanoScan(cam.Camera):
	"""Provides interface to the NanoScan 2s Pyro/9/5"""

	def __init__(self, devMode: bool = False, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.devMode = devMode

		# self.dummyapp = QtWidgets.QApplication([''])

		# Early Binding: NanoScanII.INanoScanII
		# We have to use Late Binding
		# self.NS = QAxContainer.QAxWidget("photon-nanoscan")  # {FAAD0D22-C718-459A-81CA-268CCF188807}
		# print(self.NS.dynamicCall("NsAsGetDeviceID()"))

		# ui = QtCore.QMetaType(36) # ushort https://doc.qt.io/qt-5/qmetatype.html
		ui = QtCore.QMetaType(31) # voidstar https://doc.qt.io/qt-5/qmetatype.html
		# ui = np.array([-1], dtype=np.int16)
		# ui = ctypes.c_short(-1)

		x = self.NS.dynamicCall("NsAsGetNumDevices", ui)
		print(x, ui)

		# x = 10
		# self.NS = wc.Dispatch("photon-nanoscan")
		# self.NS.NsAsGetNumDevices(ui)
		# print(ui)
				

	def __exit__(self, e_type, e_val, traceback):
		return super().__exit__(e_type, e_val, traceback)

if __name__ == '__main__':
    with NanoScan() as n:
        print("with Nanoscan as n")
        import code; code.interact(local=locals())