#!/usr/bin/env python3

import sys, os
from matplotlib import pyplot
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "src"))
sys.path.insert(0, root_dir)

import pandas as pd
import numpy as np
import fitting.fitter
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

print(f"World: {size}")