#!/usr/bin/gnuplot

set term epscairo color size 6in, 4in
set output "oscillator.eps"

set decimalsign locale 'de_DE.UTF-8'
# set datafile separator "; "
set key autotitle columnhead

set title "Oscillator Profile x-axis"
set ylabel "w_0"
set xlabel "Position"

set mxtics
set mytics
set samples 10000

w_0        = 142   # in um
z_0        = 205   # in mm
m_sq_lmbda = 2300  # in nm
# lmbda = 2300

w(x) = w_0 * sqrt((1 + ((x - z_0)**2)*(((m_sq_lmbda)/(pi * (w_0**2)))**2)))

# (x, y, xdelta, ydelta)
# fit w(x) "./data/oscillator/data_oscillator.gnu.txt" u ($1 * 10e-3):($2 * 10e-6):($1 * 0.01):($2 * 0.01) xyerrors via w_0, z_0, m_sq, lmbda
# fit w(x) "../data/oscillator/data_oscillator.gnu.txt" u ($1 * 10e-3):($2 * 10e-6) via w_0, z_0, m_sq_lmbda
fit w(x) "../data/oscillator/data_oscillator.gnu.txt" u 1:2 via w_0, z_0, m_sq_lmbda

set key bottom right spacing 2

# plot w(x) title "w(z) fit" lc rgb 'dark-magenta', \
# 	"../data/oscillator/data_oscillator.gnu.txt" u ($1 * 10e-3):($2 * 10e-6) title "Datapoints" pointtype 0 lc rgb 'dark-goldenrod'

plot w(x) title "w(z) fit" lc rgb 'dark-magenta', \
	"../data/oscillator/data_oscillator.gnu.txt" u 1:2 title "Datapoints" pointtype 0 lc rgb 'dark-goldenrod'

# plot "./data/oscillator/data_oscillator.gnu.txt" u ($1 * 10e-3):($2 * 10e-6) title "Datapoints" pointtype 0 lc rgb 'dark-goldenrod'