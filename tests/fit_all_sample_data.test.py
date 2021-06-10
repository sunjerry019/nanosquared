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
		oscillator_data["position[mm]"] / np.power(10, 3),
		oscillator_data["position[mm]"] / np.power(10, 3),
		diode_data_fast["position[mm]"] / np.power(10, 3),
		diode_data_slow["position[cm]"] / np.power(10, 2),
	]
ys     = [
		oscillator_data["diam_x[um]"]   / (np.power(10, 6) * 2),
		oscillator_data["diam_y[um]"]   / (np.power(10, 6) * 2),
		diode_data_fast["diam_y[um]"]   / (np.power(10, 6) * 2),
		diode_data_slow["diam_x[um]"]   / (np.power(10, 6) * 2),
	]
wvs     = np.array([2300e-9, 2300e-9, 1650e-9, 1650e-9], dtype = np.float64)
wvs_err = np.zeros(4)

xs_e    = [0.5e-3] * 4
ys_e    = [0.25e-6, 0.25e-6, 1e-6, 1e-6]

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
	# f.printOutput()
	print(labels[i], f.m_squared, '\n')