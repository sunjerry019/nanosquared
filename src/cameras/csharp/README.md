# NanoScanLibrary

This C\# Project is meant to provide a C\#.NET DLL that can be access by Python. It is simply a wrapper over the C\#.NET Interop DLL provided by MKS Ophir Optics. 

## Specifications
This is a 32-bit Class Library project with `netstandard2.0` as the target framework. To use the DLL, you need:
```
NanoScanLibrary.dll
NS2_interop.dll
```
Both of these must be in the same folder. Additionally, the scanhead must be of the PRO Version. 

## Motivation
After discussing with the lead software engineering in-charge of maintaining this software at MKS Ophir Optics, we came to the conclusion that many functions just do not work well between that particular ActiveX COM interface and Python. One particular error was an error in `pywin32` that results in by-ref parameters being passed wrongly to the COM interface. This error was only fixed in version `300`, which is not available to us right now.

In any case, Python can use C\#.NET DLLs through `pythonnet` very well and this particular ActiveX COM Interface works decently well in C\#. This sub-project therefore **serves to wrap the interop DLL in a way that can be accessed by Python**, thereby saving a lot of work trying to find workarounds to make things work.

## Scheme of Operation
```
Python -> C# -> ActiveX COM -> NanoScan Software -> Scanhead
```
where C\# will be doing most of the heavy-lifting. 

This requires that the scanhead be upgraded to the PRO licence. The licence is written to the EEPROM in the scanhead and read by the NanoScan software. 

If the scanhead is properly activated with the PRO Licence, then the software will forward the API calls from the ActiveX Endpoint to the scanhead. 

Do note that due to limitations of `msl-loadlib`, no GUI functions seem to be available. 

## Documentation
Resources available are:
- `NanoScan.cs`, which provides the methods
- The Automation Developer Guide provided in the NanoScan Automation Folder upon installation.
- The C\# Code Example in the NanoScan Automation Folder (especially if you want to change the C\# code itself)

## Testing
To test if the DLL loads properly in Python, you will need a 32-bit Python environment. An example Anaconda environment file is provided as [nanoscan_32.yml](../archive/nanoscan_32.yml).