# M-Squared Automation

Automated M-Squared Scanner and Profiler using the WinCamD / Nanoscan Camera.

# Models

The WinCamD Camera used is the [WinCamD-IR-BB](https://dataray.com/collections/beam-profiling-cameras/products/wincamd-ir-bb-broadband-2-to-16-%C2%B5m-mwir-fir-beam-profiler).

# How it works
## Measuring Beam-Width Data
## Fitting the Data

# Logging
All logging is provided by the `LoggerMixIn` class under `common/helpers.py`. All component classes inherit `LoggerMixIn`, which provides the method `self.log()`. This allows easy control of the log level and the way logging is handled in the entire project. 

# Code Linting in VS Code

Refer to https://stackoverflow.com/a/54488818 for taming PyLint. In particular, you can do:
```json
"python.linting.pylintArgs": [
		"--max-line-length=80",
		"--disable=all",
		"--enable=F,E,unreachable,duplicate-key,unnecessary-semicolon,global-variable-not-assigned,unused-variable,binary-op-exception,bad-format-string,anomalous-backslash-in-string,bad-open-mode",
		"--disable=W0142,W0403,W0613,W0232,R0903,R0913,C0103,R0914,C0304,F0401,W0402,E1101,W0614,C0111,C0301"
	]	
```