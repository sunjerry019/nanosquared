# Nanoscan M-Squared Automation

Automated M-Squared Scanner and Profiler using the WinCamD / Nanoscan Camera.

## Models

The WinCamD Camera used is the [WinCamD-IR-BB](https://dataray.com/collections/beam-profiling-cameras/products/wincamd-ir-bb-broadband-2-to-16-%C2%B5m-mwir-fir-beam-profiler). 

The controller used for this project is the SIGMAKOKI/OptoSigma Controller `GSC-01` with the accompanying stage `SGSP26-200`.

## Extending this code

The code responsible for communicating with each component are separated into different modules, which can be imported into a combination script (currently WIP on branch [combination](https://github.com/sunjerry019/nanosquared/tree/combination)). As OOP concepts have always been the core to the design of this software, any new stage/beam profiler can easily be integrated into the project by extending the base classes. 

Refer to [fitting](https://github.com/sunjerry019/nanosquared/tree/master/fitting) for documentation on the fitting module. 

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
