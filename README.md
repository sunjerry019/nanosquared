# M-Squared Automation
Automated M-Squared Scanner and Profiler using the WinCamD / Nanoscan Camera.

## Important Note
This repository also contains code to interact with the WinCamD and Nanoscan Beam Profiler. These functions may be used independent of the M² Measurement code.

See below for more information on how to use it.

## Supported Models
The WinCamD Camera used is the [DataRay WinCamD-IR-BB](https://dataray.com/collections/beam-profiling-cameras/products/wincamd-ir-bb-broadband-2-to-16-%C2%B5m-mwir-fir-beam-profiler). 

The NanoScan Camera used is the [Ophir NanoScan 2s Pyro/9/5](https://www.ophiropt.com/laser--measurement/beam-profilers/products/Scanning-Slit-Beam-Profiling-with-NanoScan/NanoScan-2s-Pyro-9-5). You will need the PRO version instead of the STD Version. The activation code is device-specific and written into the EEPROM of the Scanhead. 

The controller used for this project is the SIGMAKOKI/OptoSigma Controller `GSC-01` with the accompanying stage `SGSP26-200`.

Due to software compability issues, device-interfacing code in this repository may only run on Windows. 

## How it works
### Measuring Beam-Width Data
### Fitting the Data
The `Fitter` module under [fitting](./src/fitting) is used to fit the data obtained. 
```
Fitter ┬─> ODRFitter (scipy.odr):                optimizes x and y-error
       ├─> OCFFitter (scipy.optimize.curve_fit): optimizes y-error
       │
    ┌──┴───> MsqODRFitter / MsqOCFFitter: Provides all functionalities
    │                                     and fitting using the selected 
    │                                     fitting method
    │
MsqFitter: Provides functionalities common to all fitting methods
```
There are 2 different fitters available (see above). See [fitting](./src/fitting) for more details on the fitting modes available to obtain M² (M²λ, M² and ISO modes). 

The default fitting method is `scipy.optimize.curve_fit`. 

By default, we do not use the fit equation described in ISO 11146-1:2021 Section 9 due its large errors. Instead, we use the *M² Mode*, which fits the obtained caustic to the guassian beam equation:
<p align="center"><img src="https://latex.codecogs.com/svg.image?\bg_white&space;\omega(z)&space;=&space;\omega_0&space;\sqrt{1&space;&plus;&space;(z&space;-&space;z_0)^2\left(\frac{M^2\lambda}{\pi\omega_0^2}\right)^2}" title="\bg_white \omega(z) = \omega_0 \sqrt{1 + (z - z_0)^2\left(\frac{M^2\lambda}{\pi\omega_0^2}\right)^2}" /></p>
This obtains the M² parameter as one of the fit parameters. 

### Logging
All logging is provided by the `LoggerMixIn` class under `common/helpers.py`. All component classes inherit `LoggerMixIn`, which provides the method `self.log()`. This allows easy control of the log level and the way logging is handled in the entire project. 

## Extending this code
The code responsible for communicating with each component are separated into different modules, which can be imported into a combination script. As OOP concepts have always been the core to the design of this software, any new stage/beam profiler can easily be integrated into the project by extending the base classes. 

Refer to [fitting](./src/fitting) for documentation on the fitting module, and how you might can extend it to suit your purposes. 

## Version Information
For Python packages used, refer to `conda-environment.yml`. 

The DataRay Software versions used for the development of this code are as follows:
- 32-bit: [iDataRay80D63](https://dataray-web.s3.amazonaws.com/sw/iDataRay80D63.zip)
- 64-bit: [iDataRay80D62_x64](https://dataray-web.s3.amazonaws.com/sw/iDataRay80D62_x64.zip)

The NanoScan Software version is: `v2.9.1.28`.

## Installation
### NanoScan
To use the `NanoScan` Python Interface, you first need to install the `NanoScan` software. A [copy](./installers) of which lives in this repository for archival purposes.

Due to some security policy, loading a DLL from a network location may be disabled on certain computers. In this case, copy `NanoScanLibrary.dll` and `NS2_Interop.dll` to `C:\nanosquared_include\` and it should load fine. The scripts are written in such a way as to fall back to that location (This behaviour may change in the future).

*More to be added*

### WinCamD
To use the `WinCamD` Python Interface, you first need to the install `DataRay` software. Please install the version that corresponds to your Python installation (i.e. 64-bit DataRay for 64-bit Python). As DataRay is regularly putting out updates for their devices, we have decided not to include the installer in this repository. Please visit their website for more information. 

*More to be added*

## Independent Modules
*more to be added, describing which modules may be used independently*

## Troubleshooting
### WinCamD is not giving my any data/no DataReady events are fired
This could be because there are some limitation on the number of devices that can be plugged into one set of USB ports on the computer. Try plugging the stage and WinCamD to separate sides of the computer/laptop.

### NanoScan is only giving me -0.1 as the beamwidth
*Note: This could also manifest as nothing happening after requesting a beam width reading. This is because the software is waiting for sensible data as part of the `wait_stable` subroutine.*

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