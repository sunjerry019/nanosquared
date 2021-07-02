#!/usr/bin/env python3

import os,sys

import comtypes
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam

import comtypes
import comtypes.client as cc

import logging
import gc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class WinCamD(cam.Camera):
	def __init__(self):
		self.dataControl = cc.CreateObject("DATARAYOCX.GetDataCtrl.1")
		self.dataControl.StartDriver()
	
	def __exit__(self, e_type, e_val, traceback):
		del self.dataControl
		gc.collect()
		return super().__exit__(e_type, e_val, traceback)

if __name__ == '__main__':
    with WinCamD() as w:
        print("with WinCamD as w")
        import code; code.interact(local=locals())