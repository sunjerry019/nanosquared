import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

for name in glob.glob('./dataset*.dat'):
    data = pd.read_csv(name, sep=",", header = 0)

    x = data['x'].to_numpy()
    horizontal = np.arange(len(x))

    plt.plot(horizontal, x, 'r+:', label = "Raw Data")

    plt.ylabel('Beam Diam [um]')
    plt.xlabel('Measurement number')
    plt.legend(loc = "upper center", bbox_to_anchor=(1.2, 1))
    plt.tight_layout()
    plt.show()
    plt.clf()