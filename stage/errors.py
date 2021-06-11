#!/usr/bin/env python3

import warnings
from functools import wraps 
# https://stackoverflow.com/q/30846363
# https://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html
# https://stackoverflow.com/a/11731208

class ControllerError(Exception):
    """Raised when there is an error when sending commands to the controller"""

class PositionOutOfBounds(Exception):
    """Raised when the position given is out of bounds of what the controller supports"""

def FailSilently(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        try:
            return method(self, *method_args, **method_kwargs)
        except ControllerError:
            pass

    return _impl

def FailWithWarning(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        try:
            return method(self, *method_args, **method_kwargs)
        except ControllerError as e:
            warnings.warn(f"Command failed with error:\n{e}")

    return _impl


