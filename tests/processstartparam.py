#!/usr/bin/env python3

import sys, os
from matplotlib import pyplot
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "src", "nanosquared"))
sys.path.insert(0, root_dir)

import pandas as pd
import numpy as np
import fitting.fitter
from mpi4py import MPI

# == BEGIN SETTINGS ==
NUM_X = 100
NUM_Y = 100
BEREICH = 10
slow_axis = False
# ==  END  SETTINGS ==

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

total = NUM_X * NUM_Y
chunksize = int(np.floor(total / size))

eachNode    = [chunksize] * size  
eachNode[0] = total - (size - 1) * chunksize
# the number of datapoints each node should get
# The main node gets more

chunks  = None

print(f"World: {size}, Chunksize: {eachNode[rank]}")

if rank == 0:

	if slow_axis:
		diode_data_fast = pd.read_csv('../data/diode/slow_axis.txt', delimiter = '; ', engine='python', decimal=",")	
		x = diode_data_fast["position[cm]"] * 10
		y = diode_data_fast["diam_x[um]"] / 2
	else:
		diode_data_fast = pd.read_csv('../data/diode/fast_axis.txt', delimiter = '; ', engine='python', decimal=",")	
		x = diode_data_fast["position[mm]"]
		y = diode_data_fast["diam_y[um]"] / 2

	min_w = np.argmin(y)

	z_0 = x[min_w]
	w_0 = y[min_w]
	
	# Variation
	z_0_values = z_0 + np.linspace(-BEREICH, BEREICH, endpoint=True, num = NUM_X, dtype = 'float64')
	w_0_values = w_0 + np.linspace(-BEREICH, BEREICH, endpoint=True, num = NUM_Y, dtype = 'float64')
	
	# https://stackoverflow.com/a/11144716
	# Cartesian Product
	allcombi = np.transpose([np.tile(z_0_values, len(w_0_values)), np.repeat(w_0_values, len(z_0_values))])
	
	# Split into chunks for scattering
	chunks = np.array(np.split(allcombi, np.cumsum(eachNode))[:-1])
	print(chunks.shape)
	# has length = size
	# Remove the last one because it is an empty array
else:
	x = np.empty(19, dtype='float64')
	y = np.empty(19, dtype='float64')

x = comm.bcast(x, root=0)
y = comm.bcast(y, root=0)

# https://mpi4py.readthedocs.io/en/stable/tutorial.html > Scattering numpy array
mychunk = np.empty((eachNode[rank], 2) , dtype='float64')
comm.Scatter(chunks, mychunk, root=0)

print(f"{rank}: shape = {mychunk.shape}")

f = fitting.fitter.MsqODRFitter(
	x              = x, 
	y              = y, 
	xerror         = 0.5,
	yerror         = 1,
	wavelength     = 1650,
	wavelength_err = 0,
	mode           = 0
)
print(f"{rank}: Processing start")

results = []

for (z_0, w_0) in mychunk:
	f.setInitialGuesses(w_0 = w_0, z_0 = z_0)
	f.fit()

	if (f.output.info >= 4):
		result = {
			"init": (str(z_0), str(w_0)),
			"m2"  : ['0', '0'], 
			"beta": [str(i) for i in f.output.beta]
		}
	else:
		result = {
			"init": (str(z_0), str(w_0)),
			"m2"  : [str(i) for i in f.m_squared], 
			"beta": [str(i) for i in f.output.beta]
		}

	results.append(result)

print(f"{rank}: Processing end")
comm.Barrier()

results = comm.gather(results, root=0)

if rank == 0:
	# Collapse the list of results from each node into one big list
	results = [item for sublist in results for item in sublist]

	filename = f"/home/y/Yudong.Sun/attoworld/slurm/{'slow' if slow_axis else 'fast'}_axis.ignore.out" 
		
	with open(filename, 'w') as f:
		f.write("# init_z\tinit_w\tm2\tdm2\tbeta\n")
		for res in results:
			init = '\t'.join(res['init'])
			m2   = '\t'.join(res['m2'])
			beta = '\t'.join(res['beta'])
			f.write("{}\t{}\t{}\n".format(init, m2, beta))
