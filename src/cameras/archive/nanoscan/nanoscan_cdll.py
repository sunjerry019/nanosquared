import ctypes

# x = ctypes.LibraryLoader("NS2_interop.dll")
# print(x.NsInteropGetNumDevices)

x = ctypes.CDLL("NSIO.dll")
print(x)