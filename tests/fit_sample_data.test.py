#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.abspath(".."))

import pandas as pd
import numpy as np
import fitter

data = pd.read_csv('../data/oscillator/data_oscillator.txt', delimiter = '; ', engine='python', decimal=",")

print(data.columns)

print("X-Axis")
x = data["position[mm]"] / np.power(10, 3)
y = data["diam_x[um]"]   / (np.power(10, 6) * 2)

f = fitter.Fitter(
	x      = x, 
	y      = y, 
	xerror = lambda x: 0.01*x, 
	yerror = lambda y: 0.01*y
)

w_0   = 142e-6
z_0   = 205e-3
m_sq  = 1
lmbda = 2300e-9

m_sq_lmbda = m_sq * lmbda

f.fit(initial_params = np.array([w_0, z_0, m_sq_lmbda]))
f.printOutput()