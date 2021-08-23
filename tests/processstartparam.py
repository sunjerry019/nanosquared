#!/usr/bin/env python3

import sys, os
from matplotlib import pyplot
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import pandas as pd
import numpy as np
import fitting.fitter
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
	diode_data_fast = pd.read_csv('../data/diode/fast_axis.txt', delimiter = '; ', engine='python', decimal=",")	
	x = diode_data_fast["position[mm]"]
	y = diode_data_fast["diam_y[um]"] / 2
else:
	x = np.empty(19, dtype='float64')
	y = np.empty(19, dtype='float64')

x = comm.bcast(x, root=0)
y = comm.bcast(y, root=0)

print(f"{rank}: {x[0]}, {y[0]}")

# f = fitting.fitter.MsqFitter(
# 	x              = diode_data_fast["position[mm]"], 
# 	y              = diode_data_fast["diam_y[um]"] / 2, 
# 	xerror         = 0.5,
# 	yerror         = 1,
# 	wavelength     = 1650,
# 	wavelength_err = 0
# )

# f.setInitialGuesses(rank, rank)
# print(f"Received {f.initial_guesses}")

# f.estimateInitialGuesses()
# f.printOutput()