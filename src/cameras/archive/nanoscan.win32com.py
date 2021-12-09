#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam

import win32com
import win32com.client as wc
# import nanoscan_genpy as NSAx # does not work

import logging

class NanoScan(cam.Camera):
	"""Provides interface to the NanoScan 2s Pyro/9/5"""

	def __init__(self, devMode: bool = False, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.devMode = devMode

		# Early Binding: NanoScanII.INanoScanII
		# We have to use Late Binding
		self.NS = wc.Dispatch("photon-nanoscan")

		# ui = QtCore.QMetaType(36) # ushort https://doc.qt.io/qt-5/qmetatype.html
		# ui = QtCore.QMetaType(31) # voidstar https://doc.qt.io/qt-5/qmetatype.html
		# ui = np.array([-1], dtype=np.int16)
		# ui = ctypes.c_short(-1)

		numDevices = -1
		self.NS.NsAsGetNumDevices(numDevices)
		print(numDevices)

	def __exit__(self, e_type, e_val, traceback):
		return super().__exit__(e_type, e_val, traceback)

if __name__ == '__main__':
    with NanoScan() as n:
        print("with Nanoscan as n")
        import code; code.interact(local=locals())