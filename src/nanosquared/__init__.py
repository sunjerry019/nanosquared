# Reference: https://stackoverflow.com/a/13254248/3211506

import os, sys
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import common
import cameras
import fitting
import stage
import measurement