#!/usr/bin/env python3

import sys, os
from matplotlib import pyplot
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
sys.path.insert(0, root_dir)

import pandas as pd
import numpy as np
import fitting.fitter
from mpi4py import MPI

# == BEGIN SETTINGS ==
NUM_X = 100
NUM_Y = 100
BEREICH = 10
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

print(f"{rank}:\tWorld: {size}, Chunksize: {eachNode[rank]}")

def processFile(filename):
	# Init
	
	numpoints = 0
	chunks = None
	x = None
	y = None

	if rank == 0:
		data = pd.read_csv(filename, delimiter = '; ', engine='python', decimal=",")	
		x = data["position[mm]"]
		y = data["diameter[um]"] / 2

		numpoints = len(x)

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

	numpoints = comm.bcast(numpoints, root = 0)
	if rank != 0:
		x = np.empty(numpoints, dtype='float64')
		y = np.empty(numpoints, dtype='float64')

	x = comm.bcast(x, root = 0)
	y = comm.bcast(y, root = 0)

	# https://mpi4py.readthedocs.io/en/stable/tutorial.html > Scattering numpy array
	mychunk = np.empty((eachNode[rank], 2) , dtype='float64')
	comm.Scatter(chunks, mychunk, root=0)

	print(f"{rank}: shape = {mychunk.shape}")
	
	f = fitting.fitter.MsqOCFFitter(
		x              = x, 
		y              = y, 
		# xerror         = 0.5,
		yerror         = lambda y: 0.01*y, # 1% error
		wavelength     = 1650,
		wavelength_err = 0,
		mode           = fitting.fitter.MsqFitter.M2_MODE
	)
	print(f"{rank}: Processing start")

	results = []

	for (z_0, w_0) in mychunk:
		nofit = False

		f.setInitialGuesses(w_0 = w_0, z_0 = z_0)
		try:
			f.fit()
		except RuntimeError as e:
			nofit = True
			print(f"{(z_0, w_0)}: Did not converge: {e}")

		if (nofit or
		    (isinstance(f, fitting.fitter.ODRFitter) and f.output.info >= 4) or
		    (isinstance(f, fitting.fitter.OCFFitter) and ((not np.isfinite(f.output.sd_beta).any()) or f.m_squared[0] < 1))
		):
			result = {
				"init": (str(z_0), str(w_0)),
				"m2"  : ['0', '0'], 
				"beta": ['0', '0', '0'] if nofit else [str(i) for i in f.output.beta]
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

		filename = f"/home/y/Yudong.Sun/attoworld/slurm/{os.path.basename(filename)}.ignore.tsv" 
			
		with open(filename, 'w') as f:
			f.write("# init_z\tinit_w\tm2\tdm2\tbeta\n")
			for res in results:
				init = '\t'.join(res['init'])
				m2   = '\t'.join(res['m2'])
				beta = '\t'.join(res['beta'])
				f.write("{}\t{}\t{}\n".format(init, m2, beta))

import glob
pfad = os.path.join(root_dir, "data", "2021-09-02_Testdata", "*.txt")

for filename in glob.iglob(pfad, recursive=False):
	if rank == 0: 
		print(f"Processing file {filename}")

	processFile(filename)
	comm.Barrier()
	
	if rank == 0: 
		print(f"Finished file {filename}")
	