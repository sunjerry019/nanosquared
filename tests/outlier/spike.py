#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

data = pd.read_csv("dataset_42.dat", sep=",", header = 0)

x = data['x'].to_numpy()
horizontal = np.arange(len(x))
print(x)

def remove_spikes(arr: np.ndarray, threshold: float) -> np.ndarray:
    # We make use of a circular wrap-around
    # https://stackoverflow.com/questions/17739543/wrapping-around-slices-in-python-numpy
    # d = np.diff(arr, append = arr[0]) # Wrap-around
    # l = len(arr)
    # ret = []
    # for i in range(l):
    #     r = range(i-1, i+1)
    #     neighs = d.take(r, mode='wrap')
    #     # if np.abs(neighs)

    peaks, properties = scipy.signal.find_peaks(arr, prominence = threshold)
    print(properties)
    left_bases  = properties["left_bases"]
    right_bases = properties["right_bases"] 

    within_peak = []
    for i in range(len(peaks)):
        within_peak.append(np.arange(left_bases[i] + 1, right_bases[i]))

    within_peak = np.unique(np.concatenate(within_peak))
    
    print(within_peak)

    # plt.plot(np.arange(len(arr)), arr, 'b+:')
    # plt.plot(peaks, arr.take(peaks), "ro")
    # plt.ylabel('Beam Diam [um]')
    # plt.xlabel('Time [sec]')
    # plt.show()
    # plt.clf()

        
    return arr
    return np.array(ret)

def get_hist(x):
    hist, bin_edges = np.histogram(x, bins = 30)
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

