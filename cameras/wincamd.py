#!/usr/bin/env python3

import os,sys
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import cameras.camera as cam

class WinCamD(cam.Camera):
	def __init__(self):
		pass