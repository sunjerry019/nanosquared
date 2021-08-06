#!/usr/bin/env python3

import sys, os
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import pandas as pd
import numpy as np
import fitting.fitter

oscillator_data = pd.read_csv('../data/oscillator/data_oscillator.txt', delimiter = '; ', engine='python', decimal=",")
diode_data_fast = pd.read_csv('../data/diode/fast_axis.txt', delimiter = '; ', engine='python', decimal=",")
diode_data_slow = pd.read_csv('../data/diode/slow_axis.txt', delimiter = '; ', engine='python', decimal=",")

# Prepare pairs to fit
labels = ["Oscillator X-Axis", "Oscillator Y-Axis", "Diode Slow Axis", "Diode Fast Axis"]
xs     = [
		oscillator_data["position[mm]"],
		oscillator_data["position[mm]"],
		diode_data_fast["position[mm]"],
		diode_data_slow["position[cm]"] * 10,
	]
ys     = [
		oscillator_data["diam_x[um]"] / 2,
		oscillator_data["diam_y[um]"] / 2,
		diode_data_fast["diam_y[um]"] / 2,
		diode_data_slow["diam_x[um]"] / 2,
	]
wvs     = np.array([2300, 2300, 1650, 1650], dtype = np.float64)
wvs_err = np.zeros(4)

xs_e    = [0.5] * 4
ys_e    = [0.25, 0.25, 1, 1]

for i in range(len(labels)):
	f = fitting.fitter.MsqFitter(
		x              = xs[i], 
		y              = ys[i], 
		xerror         = xs_e[i],
		yerror         = ys_e[i],
		wavelength     = wvs[i],
		wavelength_err = wvs_err[i]
	)

	f.estimateAndFit()
	f.printOutput()
	print(labels[i], f.m_squared, '\n')
	fig, ax = f.getPlotOfFit()
	fig.show()
	break