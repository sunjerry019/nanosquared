#!/usr/bin/env python3
import os,sys
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import stage.errors
import common.helpers as h

import abc
from collections import namedtuple

class Stage(abc.ABC):
    LIMIT_UPPER = 0
    LIMIT_LOWER = 0
    
    def __init__(self, pos = 0):
        """Stage Object to store position and other parameters of the stage

        Parameters
        ----------
        pos : number, optional
            Initial position of the stage, by default 0
        """
        self._position = 0
        self.position = pos

        # Sets whether or not the position data in the stage object is dirty (i.e not reliable)
        self._dirty     = False
        self._permDirty = False
        self.ranged     = False # Sets whether we can trust the LIMIT_UPPER and LIMIT_LOWER

    @abc.abstractmethod
    def setLimits(self, upper, lower):
        """Sets the lower and upper limit. Also here just so that this class may not be instantiated.

        Parameters
        ----------
        upper : number
            Upper limit
        lower : number
            Lower limit
        
        Raises
        ------
        ValueError
            Raised when upper limit is lower than lower limit

        """

        if (upper < lower):
            raise ValueError("Given upper limit lower than given lower limit")
        
        self.LIMIT_LOWER = lower
        self.LIMIT_upper = upper

    @property
    def permDirty(self):
        return self._permDirty

    @permDirty.setter
    def permDirty(self, isPermDirty: bool):
        """Provides the permDirty flag.
        
        Once PermDirty, always PermDirty unless homed. 

        Stage position becomes permanently dirty, when the controller itself is no longer
        tracking it, e.g. after the motor has been freed.
        """
        self.dirty = True
        self._permDirty = True

    @property
    def dirty(self):
        return self._dirty
    
    @dirty.setter
    def dirty(self, isDirty: bool):
        """Provides the dirty flag.
        
        Stage position is dirty when the jog command it used, as we cannot keep track of 
        how many pulses the stage has moved during the jog. 

        The position can be cleaned again by syncing with the controller. See `GSC01.syncPosition()` 
        for an example
        """
        if not self.permDirty:
            self._dirty = isDirty
        elif isDirty:
            raise stage.errors.PositionDirtyError("PermDirty, rehome stage.")
    
    @property
    def position(self):
        if not self.dirty:
            return self._position
        else:
            raise stage.errors.PositionDirtyError("Please sync stage position.")
    
    @position.setter
    def position(self, x):
        return self.positionSetter(x = x)
        
    def positionSetter(self, x):
        """Checks if the position to be set is within range and sets it,
        Should be run before executing any moves

        !Unsafe state: if position is dirty but the dirty flag is not set/unset.

        Parameters
        ----------
        x : number
            Position; Position must be a number between self.LIMIT_LOWER and self.LIMIT_UPPER

        Raises
        ------
        stage.errors.PositionOutOfBoundsError
            Raised when the given x is not within the bounds set by the controller

        """
        
        if (self.LIMIT_LOWER <= x <= self.LIMIT_UPPER):
            self._position = x
        else:
            raise stage.errors.PositionOutOfBoundsError(f"Position must be between {self.LIMIT_LOWER} and {self.LIMIT_UPPER}")

class GSC01_Stage(Stage):
    LIMIT_UPPER =  16777215
    LIMIT_LOWER = -16777215

    def __init__(self, pos: int = 0):
        """Stage Object to store position and other parameters of the stage

        Parameters
        ----------
        pos : int, optional
            Initial position of the stage, by default 0
        """

        super().__init__(pos = pos) 

        self.pulseRange = 1
        self.travel     = 1

        speed = {
            "jog": 0,
            "min": 0,
            "max": 0
        } 
        # In PulsePerSecond
        # Set speed in units of 100 PPS. Values less than 100 PPS are rounded down
        # For additional documentation see GSC01.setSpeed()

        self.speed    = namedtuple("StageSpeed", speed.keys())(*speed.values())
        self.acdcTime = 0 # in milisecond

    def setLimits(self, upper: int, lower: int):
        """We should not need this method, but I implement it just so that this will instantiate

        Parameters
        ----------
        upper : int
            Upper limit
        lower : int
            Lower limit
        """

        super().setLimits(upper = upper, lower = lower)
    
    # https://stackoverflow.com/q/3336767 Does not work, hence ugly workaround
    def positionSetter(self, x: int):
        """Checks if the position to be set is within range and sets it,
        Should be run before executing any moves

        Parameters
        ----------
        x : int
            Position; Position must be a number between -16,777,215 and 16,777,215

        Raises
        ------
        stage.errors.PositionOutOfBoundsError
            Raised when the given x is not within the bounds set by the controller
        
        TypeError
            Raised when the given x is not an integer

        """

        super().positionSetter(x = h.ensureInt(x))
    
    def recalculateUmPerPulse(self):
        """Recalculates the um_per_pulse after setting `self.pulseRange`
        
        `self.pulseRange` needs to be set beforehand.
        """
        self.um_per_pulse = (self.travel * 1000) / self.pulseRange

    def resetStage(self):
        """Meant to set the upper and lower limit based on pulseRange after homing
        """

        return self.setLimits(lower = -16777215, upper = 16777215)

class SGSP26_200(GSC01_Stage):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.travel     = 200 # mm
        self.pulseRange = 100557            # This is an approximate value, since the stage is abit temperamental
        self.recalculateUmPerPulse()

    def resetStage(self):
        upper = (self.pulseRange - 1) / 2
        lower = - upper

        return self.setLimits(lower = lower, upper = upper)

    