from msl.loadlib import LoadLibrary

# We must publish as netstandard2.0
net = LoadLibrary("./csharp/NanoScanLibrary/bin/Release/netstandard2.0/NanoScanLibrary.dll", 'net')
for item in dir(net.lib):
    if not item.startswith('_'):
        attr = getattr(net.lib, item)
        print('{} {}'.format(item, type(attr)))

print(net.lib.NanoScanLibrary.NanoScan.InitNs())