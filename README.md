# M-Squared Automation
Automated M-Squared Scanner and Profiler using the WinCamD / Nanoscan Camera.

## Models
The WinCamD Camera used is the [DataRay WinCamD-IR-BB](https://dataray.com/collections/beam-profiling-cameras/products/wincamd-ir-bb-broadband-2-to-16-%C2%B5m-mwir-fir-beam-profiler). 

The NanoScan Camera used is the [Ophir NanoScan 2s Pyro/9/5](https://www.ophiropt.com/laser--measurement/beam-profilers/products/Scanning-Slit-Beam-Profiling-with-NanoScan/NanoScan-2s-Pyro-9-5).

The controller used for this project is the SIGMAKOKI/OptoSigma Controller `GSC-01` with the accompanying stage `SGSP26-200`.

## How it works
### Measuring Beam-Width Data
### Fitting the Data
### Logging
All logging is provided by the `LoggerMixIn` class under `common/helpers.py`. All component classes inherit `LoggerMixIn`, which provides the method `self.log()`. This allows easy control of the log level and the way logging is handled in the entire project. 

## Extending this code
The code responsible for communicating with each component are separated into different modules, which can be imported into a combination script (currently WIP on branch [combination](https://github.com/sunjerry019/nanosquared/tree/combination)). As OOP concepts have always been the core to the design of this software, any new stage/beam profiler can easily be integrated into the project by extending the base classes. 

Refer to [fitting](https://github.com/sunjerry019/nanosquared/tree/combination/src/fitting) for documentation on the fitting module. 

## Version Information
For Python packages used, refer to `conda-environment.yml`. 

The DataRay Software versions used for the development of this code are as follows:
- 32-bit: iDataRay80D63
- 64-bit: iDataRay80D62_x64

## Installation
### NanoScan
To use the `NanoScan` Python Interface, you first need to install the `NanoScan` software. A [copy](https://github.com/sunjerry019/nanosquared/tree/nanoscan/installers) of which lives in this repository for archival purposes.

Due to some security policy, loading a DLL from a network location may be disabled on certain computers. In this case, copy `NanoScanLibrary.dll` and `NS2_Interop.dll` to `C:\nanosquared_include\` and it should load fine. The scripts are written in such a way as to fall back to that location (This behaviour may change in the future).

## Troubleshooting
### WinCamD is not giving my any data/no DataReady events are fired
This could be because there are some limitation on the number of devices that can be plugged into one set of USB ports on the computer. Try plugging the stage and WinCamD to separate sides of the computer/laptop.

### NanoScan is only giving me -0.1 as the beamwidth
*Note: This could also manifest as nothing happening after requesting a beam width reading. This is because the software is waiting for sensible data as part of the `waitStable` subroutine.*

There could be many reasons this could be happening. Troubleshoot by opening the NanoScan software provided by Ophir Optics to determine if the NanoScan is even providing any form of data.

If there is no data despite starting data acquisition, then perhaps you need to plug NanoScan into another USB Port.

Another reason could be that the NS software did not close properly. Try running `nanoscan.py` directly and then:
```python
n.NS.ShutdownNS()
```
Then try to restart your original application that makes use of `NanoScan`.

## Code Linting in VS Code
Refer to https://stackoverflow.com/a/54488818 for taming PyLint. In particular, you can do:
```json
"python.linting.pylintArgs": [
		"--max-line-length=80",
		"--disable=all",
		"--enable=F,E,unreachable,duplicate-key,unnecessary-semicolon,global-variable-not-assigned,unused-variable,binary-op-exception,bad-format-string,anomalous-backslash-in-string,bad-open-mode",
		"--disable=W0142,W0403,W0613,W0232,R0903,R0913,C0103,R0914,C0304,F0401,W0402,E1101,W0614,C0111,C0301"
	]	
```

## References
https://stackoverflow.com/a/1067842