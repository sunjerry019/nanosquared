#!/usr/bin/env python3

import os, sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "../src/"))
sys.path.insert(0, root_dir)

from measurement.measure import Measurement

from cameras.nanoscan import NanoScan
from stage.controller import GSC01

global_devMode = True

n = NanoScan(devMode = global_devMode)
c = GSC01(devMode = global_devMode)

if not global_devMode:
    if not c.stage.permDirty:
        c.syncPosition()
        c.stage.ranged = True
    else:
        c.homeStage()
        c.findRange()

with Measurement(devMode = global_devMode, camera = n, controller = c) as M:
    print("with Measurement() as M")
    import code; code.interact(local=locals())

    # fn = "../data/M2/2021-12-09_161309_bcgpou2n.dat"
    # M.read_from_file(fn)

    # M.take_measurements()
    # M.fit_data(axis = M.camera.AXES.X, wavelength = 2300)
    # fig, ax = M.fitter.getPlotOfFit()
    # fig.show()




    

