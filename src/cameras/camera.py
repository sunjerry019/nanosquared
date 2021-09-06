#!/usr/bin/env python3

"""File provides the class camera that all camera types should inherit"""

class Camera():
    def __init__(self):
        self.apertureOpen = False

    def getAxis_avg_D4Sigma(self, axis, numsamples: int = 20):
        raise NotImplementedError
    
    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        pass