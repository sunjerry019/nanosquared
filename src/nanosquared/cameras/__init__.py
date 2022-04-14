import struct

# https://stackoverflow.com/a/1405971/3211506
bitness = 8 * struct.calcsize("P")

if bitness > 32:
    from . import all_constants
    from . import camera
    from . import nanoscan_constants
    from . import nanoscan
    from . import wincamd_constants
    from . import wincamd