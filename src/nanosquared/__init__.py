try:
    from . import common
    from . import cameras
    from . import fitting
    from . import stage
    from . import measurement
except ModuleNotFoundError:
    # Probably got called from msl-loadlib/Server32
    pass