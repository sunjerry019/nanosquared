import pandas as pd
import ast
import numpy as np

import os, sys
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "src"))
sys.path.insert(0, root_dir)

from nanosquared.cameras.nanoscan import NanoScan


datafile = pd.read_csv("datasets/2022-03-30_180005_75 DEG.dat", sep = '\t', skiprows = 8, header = 0)
positions = datafile["# position[mm]"].to_numpy()

dataset = []
with open("datasets/2022-03-30_180005_75 DEG_log.dat", 'r') as logfile:
    with open("datasets/2022-03-30_180005_75 DEG_unfiltered.dat", 'w') as outfile:
        outfile.write("""# Data written on 2022-03-30 at 18:00:05
# ==== Metadata ====
#	Rayleigh Length: [2.8601263  3.00333151] mm
#	Wavelength: 2350.0 nm
#	Precision (pps): 10
#	Metadata: 150mm
#	NanoScan Rotation Rate (Hz): 10.0
#   Regenerated from raw data: 2022-04-13 (With no filtering)
# ====== Data ======
# position[mm]	x_diam[um]	dx_diam[um]	y_diam[um]	dy_diam[um]
""")

        i = 0

        datapoint = None
        for line in logfile:
            line = line.strip()

            if line[:11] == "INFO: Point":
                datapoint = [[],[]]
            if line[:20] == "DEBUG: Got 1 Reading":
                xy = line.split("(x, y): ")[1]
                x, y = ast.literal_eval(xy)
                datapoint[0].append(x)
                datapoint[1].append(y)
            if line[:14] == "DEBUG: average":
                # datapoint[0] = NanoScan.remove_spikes(np.array(datapoint[0]), threshold = 0.2)
                # datapoint[1] = NanoScan.remove_spikes(np.array(datapoint[1]), threshold = 0.2)

                x_avg, x_stddev = np.average(datapoint[0]), np.std(datapoint[0])
                y_avg, y_stddev = np.average(datapoint[1]), np.std(datapoint[1])
                
                output = [positions[i], x_avg, x_stddev, y_avg, y_stddev]
                output = [str(x) for x in output]

                outfile.write("\t".join(output))
                outfile.write("\n")
                i += 1


