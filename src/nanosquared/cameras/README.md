# Cameras

## WinCamD
The list of essential files for the WinCamD include:
```python
# Base Classes
all_constants.py
camera.py
# WinCamD specific classes
wincamd_constants.py
wincamd.py
# Logging
../common/helpers.py
```

## NanoScan
See [csharp/README.md](csharp/README.md) for more information. Functions are not documented in the Python Code. All function calls are sent directly to the C\# DLL, see C\# code the documentation. 

The list of essential files for the NanoScan include:
```python
# Base Classes
all_constants.py
camera.py
# NanoScan specific files
csharp/NanoScanLibrary/bin/Release/netstandard2.0/NanoScanLibrary.dll
csharp/NanoScanLibrary/bin/Release/netstandard2.0/NS2_Interop.dll
nanoscan_constants.py
nanoscan_server.py       # Marshalls calls to 32-bit ActiveX Endpoint
nanoscan.py
# Logging
../common/helpers.py
```

TODO: Something about removing peaks

### Installation
Ensure the corresponding vendor software has been installed beforehand.

Due to some security policy, loading a DLL from a network location may be disabled on certain computers. In this case, copy `NanoScanLibrary.dll` and `NS2_Interop.dll` to `C:\nanosquared_include\` and it should load fine. The scripts are written in such a way as to fall back to that location (This behaviour may change in the future).

The code that handles the fallback is in `nanoscan_server.py`. Edit that file to change the loading location should, for example, `C:\nanosquared_include\` not be writable for you.