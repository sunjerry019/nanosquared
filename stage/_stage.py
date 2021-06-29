#!/usr/bin/env python3
import os,sys
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
sys.path.insert(0, root_dir)

import stage.errors

import abc

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
        """Once PermDirty, always PermDirty unless homed
        """
        self.dirty = True
        self._permDirty = True

    @property
    def dirty(self):
        return self._dirty
    
    @dirty.setter
    def dirty(self, isDirty: bool):
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
        stage.erors.PositionDirtyError
            Raised when the stage position is dirty

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

        # Check if integer: https://stackoverflow.com/a/48940855
        error = True
        try:
            if (int(x) == x):
                error = False
                return super().positionSetter(x = int(x))
        except (TypeError, ValueError):
            pass
        
        if error:
            raise TypeError(f"Position must be an integer, got: {x}")
