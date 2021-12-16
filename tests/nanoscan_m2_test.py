#!/usr/bin/env python3

import os, sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "../src/"))
sys.path.insert(0, root_dir)

from measurement.measure import Measurement

from cameras.nanoscan import NanoScan
from cameras.nanoscan_constants import NsAxes

n = NanoScan(devMode = False)

with Measurement(devMode = False, camera = n) as M:
    print("with Measurement() as M")
    import code; code.interact(local=locals())