from msl.loadlib import LoadLibrary
# run in 32 bit python

import clr
import System

# We must publish as netstandard2.0
try:
    net = LoadLibrary("../../csharp/NanoScanLibrary/bin/Release/netstandard2.0/NanoScanLibrary.dll", 'net')
except System.NotSupportedException as e:
    net = LoadLibrary("C:/nanosquared_include/NanoScanLibrary.dll", 'net')

for item in dir(net.lib):
    if not item.startswith('_'):
        attr = getattr(net.lib, item)
        print('{} {}'.format(item, type(attr)))

x = net.lib.NanoScanLibrary.NanoScan()
print(x.InitNS())