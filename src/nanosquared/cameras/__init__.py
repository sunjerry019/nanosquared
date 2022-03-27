try:
    from . import all_constants
    from . import camera
    from . import nanoscan_constants
    from . import nanoscan
    from . import wincamd_constants
    from . import wincamd
except ModuleNotFoundError:
    # Probably got called from msl-loadlib/Server32
    pass