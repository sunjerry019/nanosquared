#!/usr/bin/env python3

# For testing an annoying error with msl.loadlib

import os, sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "../src/", "nanosquared"))
sys.path.insert(0, root_dir)

from cameras.nanoscan import NanoScan

n = NanoScan(devMode = False)
n.getAxis_avg_D4Sigma(n.AXES.X)