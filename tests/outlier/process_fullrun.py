import pandas as pd
import ast
import numpy as np

datafile = pd.read_csv("datasets/2022-03-30_181423_01q5nq6i.dat", sep = '\t', skiprows = 8, header = 0)
positions = datafile["# position[mm]"].to_numpy()

dataset = []
with open("datasets/2022-03-30_181423_01q5nq6i_log.dat", 'r') as logfile:
    with open("datasets/2022-03-30_181423_01q5nq6i_unfiltered.dat", 'w') as outfile:
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
                x_avg, x_stddev = np.average(datapoint[0]), np.std(datapoint[0])
                y_avg, y_stddev = np.average(datapoint[1]), np.std(datapoint[1])
                
                output = [positions[i], x_avg, x_stddev, y_avg, y_stddev]
                output = [str(x) for x in output]

                outfile.write("\t".join(output))
                outfile.write("\n")
                i += 1


