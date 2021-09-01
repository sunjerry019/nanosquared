#!/usr/bin/env python3

import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import pandas as pd
import numpy as np
import fitting.fitter

data = pd.read_csv('../data/oscillator/data_oscillator.txt', delimiter = '; ', engine='python', decimal=",")

print(data.columns)

print("X-Axis")
x = data["position[mm]"] / np.power(10, 3)
y = data["diam_x[um]"]   / (np.power(10, 6) * 2)

f = fitting.fitter.MsqODRFitter(
	x              = x, 
	y              = y, 
	xerror         = lambda x: 0.01*x, 
	yerror         = lambda y: 0.01*y,
	wavelength     = 2300e-9,
	wavelength_err = 1e-9
)

f.estimateAndFit()
f.printOutput()
print(f.m_squared)