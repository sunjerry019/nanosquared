#!/usr/bin/env python3
import os,sys
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import stage.errors

class Stage():
    def __init__(self, pos: int = 0):
        """Stage Object to store position and other parameters of the stage

        Parameters
        ----------
        pos : int, optional
            Initial position of the stage, by default 0
        """
        self._position = 0
        self.position = pos
    
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, x):
        """Checks if the position to be set is within range and sets it,
        Should be run before executing any moves

        Parameters
        ----------
        x : int
            Position; Position must be an integer between -16,777,215 and 16,777,215

        Raises
        ------
        stage.errors.PositionOutOfBoundsError
            Raised when the given x is not within the bounds set by the controller

        """
        if (-16777215 <= x <= 16777215):
            self._position = x
        else:
            raise stage.errors.PositionOutOfBoundsError("Position must be between -16,777,215 and 16,777,215")