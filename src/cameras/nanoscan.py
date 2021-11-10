#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam

import logging
from PyQt5 import QtWidgets, QAxContainer, QtCore

class NanoScan(cam.Camera):
	"""Provides interface to the NanoScan 2s Pyro/9/5"""

	def __init__(self, devMode: bool = False, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.devMode = devMode

		self.dummyapp = QtWidgets.QApplication([''])

		# Early Binding: NanoScanII.INanoScanII
		# We have to use Late Binding
		self.NS = QAxContainer.QAxWidget("photon-nanoscan")  # {FAAD0D22-C718-459A-81CA-268CCF188807}

		numDevices = [-1]
		print(numDevices)
		ret = self.NS.dynamicCall("NsAsGetNumDevices(short&)", numDevices)
		print(ret, numDevices)
				

	def __exit__(self, e_type, e_val, traceback):
		return super().__exit__(e_type, e_val, traceback)

if __name__ == '__main__':
    with NanoScan() as n:
        print("with Nanoscan as n")
        import code; code.interact(local=locals())