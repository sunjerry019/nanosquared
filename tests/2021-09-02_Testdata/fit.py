#!/usr/bin/env python3

import sys, os
from matplotlib import pyplot
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import pandas as pd
import numpy as np
import fitting.fitter

import glob

pfad   = os.path.join(root_dir, "data", "2021-09-02_Testdata", "*.txt")
wv     = 1650 # nm
wv_err = 0    # nm

xs_e   = 0.5  # mm
ys_e   = 1    # um

for filename in glob.iglob(pfad, recursive=False):
    data  = pd.read_csv(filename, delimiter = '; ', engine='python', decimal=",")
    titel = os.path.basename(filename)

    f = fitting.fitter.MsqOCFFitter(
        x              = data["position[mm]"], 
        y              = data["diameter[um]"] / 2, 
        # xerror         = xs_e,
        yerror         = ys_e,
        wavelength     = wv,
        wavelength_err = wv_err,
        mode           = fitting.fitter.MsqFitter.M2_MODE
    )

    f.estimateAndFit()
    f.printOutput()
    print(f"== {titel} ==")
    print(f"initial params = {f.initial_guesses}")
    if f.mode == fitting.fitter.MsqFitter.M2LAMBDA_MODE:
        # w_0, z_0, M_sq_lambda
        print(f"w_0\t\t{f.output.beta[0]} +/- {f.output.sd_beta[0]} um")
        print(f"z_0\t\t{f.output.beta[1]} +/- {f.output.sd_beta[1]} mm")
        print(f"M_sq_lambda\t{f.output.beta[2]} +/- {f.output.sd_beta[2]}")
        print(f"> M_sq\t\t{f.m_squared}\n")
    elif f.mode == fitting.fitter.MsqFitter.M2_MODE:
        # w_0, z_0, M_sq
        print(f"w_0\t\t{f.output.beta[0]} +/- {f.output.sd_beta[0]} um")
        print(f"z_0\t\t{f.output.beta[1]} +/- {f.output.sd_beta[1]} mm")
        print(f"M_sq\t\t{f.output.beta[2]} +/- {f.output.sd_beta[2]}")
        print(f"> M_sq\t\t{f.m_squared}\n")

    fig, ax = f.getPlotOfFit()
    fig.suptitle(titel)

    pyplot.show()
    