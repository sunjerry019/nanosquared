#!/usr/bin/env python3

import sys, os
from matplotlib import pyplot
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import pandas as pd
import numpy as np
import fitting.fitter

oscillator_data = pd.read_csv('../data/oscillator/data_oscillator.txt', delimiter = '; ', engine='python', decimal=",")
diode_data_fast = pd.read_csv('../data/diode/fast_axis.txt', delimiter = '; ', engine='python', decimal=",")
diode_data_slow = pd.read_csv('../data/diode/slow_axis.txt', delimiter = '; ', engine='python', decimal=",")

# Unit Conversions
corr_x  = 1 # 10e-3  
corr_y  = 1 # 10e-6  
corr_wv = 1 # 10e-9  

# Prepare pairs to fit
labels = ["Oscillator X-Axis", "Oscillator Y-Axis", "Diode Fast Axis", "Diode Slow Axis"]
xs     = [
		corr_x * oscillator_data["position[mm]"],
		corr_x * oscillator_data["position[mm]"],
		corr_x * diode_data_fast["position[mm]"],
		corr_x * diode_data_slow["position[cm]"] * 10,
	]
ys     = [
		corr_y * oscillator_data["diam_x[um]"] / 2,
		corr_y * oscillator_data["diam_y[um]"] / 2,
		corr_y * diode_data_fast["diam_y[um]"] / 2,
		corr_y * diode_data_slow["diam_x[um]"] / 2,
	]
wvs     = corr_wv * np.array([2300, 2300, 1650, 1650], dtype = np.float64)
wvs_err = corr_wv * np.zeros(4)

xs_e    = [corr_x * 0.5] * 4
ys_e    = [0.25, 0.25, 1 , 1 ]

for i in range(len(labels)):
	f = fitting.fitter.MsqOCFFitter(
		x              = xs[i], 
		y              = corr_y * ys[i], 
		# xerror         = xs_e[i],
		yerror         = corr_y * ys_e[i],
		wavelength     = wvs[i],
		wavelength_err = wvs_err[i],
		mode           = fitting.fitter.MsqFitter.M2_MODE
	)

	f.estimateAndFit()
	f.printOutput()
	print(f"== {labels[i]} ==")
	# w_0, z_0, M_sq_lmbda
	print(f"w_0\t\t{f.output.beta[0]} +/- {f.output.sd_beta[0]} um")
	print(f"z_0\t\t{f.output.beta[1]} +/- {f.output.sd_beta[1]} mm")
	print(f"M_sq_lambda\t{f.output.beta[2]} +/- {f.output.sd_beta[2]} nm")
	print(f"M_sq\t\t{f.m_squared}\n")
	fig, ax = f.getPlotOfFit()
	fig.suptitle(labels[i])
	
	pyplot.show()