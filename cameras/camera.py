#!/usr/bin/env python3

"""File provides the class camera that all camera types should inherit"""

class Camera():
    def __init__(self):
        pass
    
    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        pass