import os, sys

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "../src/"))
sys.path.insert(0, root_dir)

from measurement.measure import Measurement

from cameras.nanoscan import NanoScan
from stage.controller import GSC01

cfg = {
    "port" : "COM13",
}

with NanoScan(devMode = False) as n:
    s = GSC01(devMode = False, devConfig = cfg)

    of = open("../data/find_center_data.dat", 'w')

    with Measurement(devMode = False, camera = n, controller = s) as M:
        of.write("# 10 pps precision\n")
        of.write("# n\tz_0_x/pss\tz_0_y/pps\t2w0/um\n")
        for i in range(5):
            center = M.find_center_xy(precision = 10)
            diam_x = M.measure_at(pos = center[0], axis = M.camera.AXES.X)
            diam_y = M.measure_at(pos = center[1], axis = M.camera.AXES.Y)

            of.write(f"{i}\t{center[0]}\t{center[1]}\t{diam_x}\t{diam_y}\n")

        of.write("\n")

        of.write("# 100 pps precision\n")
        of.write("# n\tz_0_x/pss\tz_0_y/pps\t2w0/um\n")
        for i in range(5):
            center = M.find_center_xy(precision = 100)
            diam_x = M.measure_at(pos = center[0], axis = M.camera.AXES.X)
            diam_y = M.measure_at(pos = center[1], axis = M.camera.AXES.Y)

            of.write(f"{i}\t{center[0]}\t{center[1]}\t{diam_x}\t{diam_y}\n")
        
    of.close()
