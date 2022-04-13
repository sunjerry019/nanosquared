#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import scipy.signal

data = pd.read_csv("dataset_42.dat", sep=",", header = 0)

x = data['x'].to_numpy()
horizontal = np.arange(len(x))
print(x)

# https://stackoverflow.com/a/25192640/3211506
# https://www.delftstack.com/howto/python/low-pass-filter-python/
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = scipy.signal.lfilter(b, a, data)
    return y

# # Filter requirements.
order = 6
fs = 1.0          # sample rate, Hz
cutoff = 0.4      # desired cutoff frequency of the filter, Hz

# sampling rate must be double cutoff

x_filt = butter_lowpass_filter(x, cutoff, fs, order)

f, t, Sxx = scipy.signal.spectrogram(x ,fs)

plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

# plt.plot(horizontal, x, color = "tab:blue", label = "Measured Data")
# plt.plot(horizontal, x_filt, color = "tab:green", label = "Filtered Data")
# plt.show()
# plt.clf()

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

# get_hist(x)

