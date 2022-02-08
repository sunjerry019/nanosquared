# Cameras

## WinCamD
The list of essential files for the WinCamD include:
```
# More to be included
```

## NanoScan
See [csharp/README.md](csharp/README.md) for more information. Functions are not documented in the Python Code. All function calls are sent directly to the C\# DLL, see C\# code the documentation. 

The list of essential files for the NanoScan include:
```
# More to be included
```

### Installation
Due to some security policy, loading a DLL from a network location may be disabled on certain computers. In this case, copy `NanoScanLibrary.dll` and `NS2_Interop.dll` to `C:\nanosquared_include\` and it should load fine. The scripts are written in such a way as to fall back to that location (This behaviour may change in the future).