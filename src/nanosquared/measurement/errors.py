#!/usr/bin/env python3

class ConfigurationError(Exception):
    """Raised when there is an error in the configuration."""

class StageOutOfRangeError(Exception):
    """Raised when the desired point is out of the range of the stage"""
