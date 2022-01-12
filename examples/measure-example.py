M.read_from_file('Y:\\project\\ag-pronin\\Personal\\Yudong Sun\\nanosquared\\data\\M2\\2021-12-09_161309_bcgpou2n.dat')
M.fit_data(axis = M.camera.AXES.X, wavelength="2300")
fig, axis = M.fitter.getPlotOfFit()
fig.show()