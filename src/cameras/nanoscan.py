#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import os,sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam

import logging

from msl.loadlib import Client64

class NanoScan(cam.Camera, Client64):
	"""Provides interface to the NanoScan 2s Pyro/9/5"""

	def __init__(self, devMode: bool = False, *args, **kwargs):
		cam.Camera.__init__(self, *args, **kwargs)
		Client64.__init__(self, module32='nanoscan_server.py')

		self.devMode = devMode

		# print(self.NsInteropGetNumDevices())
		# self.listClasses()

	def __getattr__(self, name):
		def send(*args, **kwargs):
			return self.request32(name, *args, **kwargs)
		return send

	def __exit__(self, e_type, e_val, traceback):
		return super().__exit__(e_type, e_val, traceback)

if __name__ == '__main__':
    with NanoScan() as n:
        print("with Nanoscan as n")
        import code; code.interact(local=locals())