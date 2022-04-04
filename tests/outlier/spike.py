#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

data = pd.read_csv("dataset_39.dat", sep=",", header = 0)

x = data['x'].to_numpy()
horizontal = np.arange(len(x))
print(x)

def remove_spikes(arr: np.ndarray, threshold: float) -> np.ndarray:
    # We make use of a circular wrap-around
    # https://stackoverflow.com/questions/17739543/wrapping-around-slices-in-python-numpy
    # d = np.diff(arr, append = arr[0]) # Wrap-around
    
    # ret = []
    # for i in range(l):
    #     r = range(i-1, i+1)
    #     neighs = d.take(r, mode='wrap')
    #     # if np.abs(neighs)

    i = 0
    horizontal = np.arange(len(arr))

    plt.plot(horizontal, arr, 'r+:', label = "raw data")
    
    arr_rem = arr
    horizontal_rem = horizontal
    while True:
        # find peaks
        peaks, _ = scipy.signal.find_peaks(arr_rem, prominence = threshold)

        if len(peaks) == 0:
            break

        # Generate masks
        l    = len(arr_rem)
        mask = np.ones(l, dtype=bool)
        mask[peaks] = False

        horizontal_rem = horizontal_rem[mask] 
        arr_rem        = arr_rem[mask]
        
        plt.plot(horizontal_rem, arr_rem, "o", label = f"Cycle {i}")
        
        i += 1

    # manually check first and last points
    l    = len(arr_rem)
    mask = np.ones(l, dtype=bool)

    d = arr_rem[0] - arr_rem[1]
    if np.abs(d) > threshold:
        mask[0] = False

    d = arr_rem[-1] - arr_rem[-2]
    if np.abs(d) > threshold:
        mask[-1] = False

    horizontal_rem = horizontal_rem[mask] 
    arr_rem        = arr_rem[mask]

    plt.plot(horizontal_rem, arr_rem, "o", label = f"Cycle Final")


    plt.ylabel('Beam Diam [um]')
    plt.xlabel('Measurement number')
    plt.legend(loc = "upper center", bbox_to_anchor=(1.2, 1))
    plt.tight_layout()
    plt.show()
    plt.clf()

    return arr_rem

def get_hist(x):
    hist, bin_edges = np.histogram(x, bins = 10)
    conv_kernel     = np.array([0.5, 0.5])
    bin_centers = np.convolve(bin_edges, conv_kernel, mode = "valid")

    width = (bin_edges[1] - bin_edges[0]) * 0.8

    plt.bar(bin_centers, hist, width = width, color = "tab:blue", label = "Measured Data")
    # plt.title(f"Histogram of distances measured\n({name})")
    # plt.ylabel("Frequency")
    # plt.xlabel("Distance (mm)")
    # plt.legend(loc = "upper left")
    # plt.legend(loc = "center left")
    # plt.savefig(f"./calibration/{name.split()[0].lower()}.eps", format = 'eps', bbox_inches='tight')
    plt.show()
    plt.clf()

rs = remove_spikes(x, 0.2 * np.average(x))

print(np.average(x), np.std(x))
print(np.average(rs), np.std(rs))
