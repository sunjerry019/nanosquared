#!/usr/bin/env python3

import os, sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "../src/"))
sys.path.insert(0, root_dir)

from measurement.measure import Measurement

from cameras.nanoscan import NanoScan
from cameras.nanoscan_constants import NsAxes

n = NanoScan(devMode = True)

with Measurement(devMode = True, camera = n) as M:
    # print("with Measurement() as M")
    # import code; code.interact(local=locals())

    fn = "../data/M2/2021-12-09_161309_bcgpou2n.dat"
    M.read_from_file(fn)