#!/usr/bin/env python3
# 32 Bit

from msl.loadlib import LoadLibrary
import ctypes

NS = LoadLibrary("NS2_Interop.dll", libtype = 'cdll')

# https://stackoverflow.com/a/54375211
# https://docs.python.org/3/library/ctypes.html#specifying-the-required-argument-types-function-prototypes

y = ctypes.c_int32(-1)

NS.lib.NsInteropGetNumDevices.restype = ctypes.c_int
y = NS.lib.InitNsInterop()

print(y)

x = ctypes.c_short(-1)
NS.lib.NsInteropGetNumDevices.argtypes = [ctypes.c_void_p]
NS.lib.NsInteropGetNumDevices.restype  = ctypes.c_int
y = NS.lib.NsInteropGetNumDevices(ctypes.byref(x))
print(x, y)