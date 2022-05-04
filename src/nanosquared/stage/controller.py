#!/usr/bin/env python3
# hashbang but it's meant to be run on windows ._.

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

# Python primary Helper to interact with a controller
# IMPT: THIS IS A HELPER FILE
# RUNNING IT DIRECTLY YIELDS INTERACTIVE TERMINAL

# Errors to be caught: RuntimeError, NotImplementedError, AssertionError

import os,sys
base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir) 

import serial # pyserial
import signal
import json
import warnings
import time
from collections import namedtuple

import numpy as np

from typing import Union, Optional
import traceback
import platform  	# for auto windows/linux detection
import abc

import stage.errors
import stage._stage as Stg

import common.helpers as h

import logging

class Controller(abc.ABC, h.LoggerMixIn):
    """Abstract Base Class for a controller"""

    def __init__(self, devMode: bool = True, implementation: bool = False):
        """

        Parameters
        ----------
        devMode : bool, optional
            To indicate whether to run in developement mode, by default True. 
            When development mode is turned on, no device communication will be started 
        subclass : bool, optional
            To indicate if calling from subclass
        """
        self.devMode = devMode

        if not implementation:
            self.stage = Stg.Stage() # which should throw an error

        self.startSignalHandlers()
    
    @abc.abstractmethod
    def move(self, pos):
        """Relative Move, to be implemented

        Parameters
        ----------
        pos : number
            Position to move to
        """
        self.stage.position = pos
        pass
    
    @abc.abstractmethod
    def rmove(self, delta):
        """Relative Move, to be implemented

        Parameters
        ----------
        delta : number
            Number of steps to move
        """
        self.stage.position += delta
        pass

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        # self.abort()
        self.closeDevice()

    @abc.abstractmethod
    def abort(self):
        pass
    
    @abc.abstractmethod
    def closeDevice(self):
        pass
    
    def startSignalHandlers(self):
        """ Starts appropriate signal handlers to handle e.g. keyboard interrupts. 
        Ensures safe exit and disconnecting of controller.
        """
        # https://stackoverflow.com/a/4205386/3211506
        signal.signal(signal.SIGINT, self.KeyboardInterruptHandler)

    def KeyboardInterruptHandler(self, signal, frame):
        """Abort and close the serial port if interrupted. 
        Handles a SIGINT according to https://docs.python.org/3/library/signal.html#signal.signal.

        Parameters
        ----------
        signal : int
            signal number
        frame : signal Frame object
            Frame objects represent execution frames. They may occur in traceback objects (see below), and are also passed to registered trace functions.
        """

        print("^C Detected: Emergency stop and closing port.")
        # print("Shutter will be closed as part of the aborting process.")
        self.abort()
        self.closeDevice()
        raise KeyboardInterrupt
        
        # print("Exiting")
        # sys.exit(1)
        # use os._exit(1) to avoid raising any SystemExit exception

class SerialController(Controller, abc.ABC):
    """Abstract Base Class for a serial controller"""

    def __init__(self, devConfig: Union[dict,str,None] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ENTER = None
        
        self.loadConfig(devConfig)
        self.initializeDevice()

    def loadConfig(self, devConfig: Union[dict,str,None] = None):
        """Load the config for device communication from either a json file or a dictionary into self.cfg

        Parameters
        ----------
        devConfig : Union[dict,str,None], optional
            json file or dictionary of configuation details, by default None

        Raises
        ------
        RuntimeError
            Raised if an invalid config file is found but self.devMode = False
        """

        cfg = {
            "port"      : "COM1",
            "baudrate"  : 9600,
            "parity"    : serial.PARITY_NONE,
            "stopbits"  : serial.STOPBITS_ONE,
            "bytesize"  : serial.EIGHTBITS,
            "timeout"   : 2
        }

        # https://stackoverflow.com/a/1857/3211506
        # Windows = Windows, Linux = Linux, Mac = Darwin
        if platform.system() == "Linux":
            cfg["port"] = '/dev/ttyUSB0'


        # We try to load device configuration if provided
        if devConfig:
            if type(devConfig) is str:
                with open(devConfig, 'r') as f:
                    devConfig = json.load(f)

            if isinstance(devConfig, dict):
                cfg.update(devConfig)
            else:
                self.log("Non-dictionary devConfig. Skipped: {}".format(devConfig), loglevel = logging.WARN)
        else:
            # We attempt to load the config from a default "config.local.json" if it exists
            base_dir = os.path.dirname(os.path.realpath(__file__))
            local_conf = os.path.join(base_dir, "config.local.json")

            if os.path.isfile(local_conf):
                try:
                    with open(local_conf, 'r') as f:
                        devConfig = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    if self.devMode:
                        self.log("Invalid local config file, not loaded!\n\nError: {}\n\n".format(e), loglevel = logging.WARN)
                    else:
                        raise RuntimeError("Invalid config.local.json found! Delete or correct errors!\n\nError: {}".format(e))
                else:
                    # We are guaranteed its a dict
                    cfg.update(devConfig)

        self.cfg = cfg

    def initializeDevice(self):
        """Initializes the serial devices and saves it into self.dev

        Raises
        ------
        RuntimeError
            Raised if unable to establish serial communication
        """
        if not self.devMode:
            try:
                # BEGIN SERIAL SETUP
                self.dev = serial.Serial(
                        port 		= self.cfg['port'],
                        baudrate 	= self.cfg['baudrate'],
                        parity 		= self.cfg['parity'],
                        stopbits    = self.cfg['stopbits'],
                        bytesize    = self.cfg['bytesize'],
                        timeout     = self.cfg['timeout']
                    )
                if self.dev.isOpen():
                    self.dev.close()
                    self.dev.open()

                time.sleep(2)
                print("Initalised serial communication")
                # END SERIAL SETUP

            except Exception as e:
                print(e)
                raise RuntimeError("Unable to establish serial communication. Please check port settings and change configuration file accordingly. For more help, consult the documention.\n\nConfig: {}\n\n{}: {}\n\n{}".format(self.cfg, type(e).__name__ , e, traceback.format_exc()))
                # sys.exit(0)
        else:
            self.dev = None
            self.log("devmode -- No serial device will be used", loglevel = logging.WARN)

    def closeDevice(self):
        """Closes the serial device connection"""
        if not self.devMode and self.dev.isOpen():
            self.dev.close()

    @abc.abstractmethod
    def send(self):
        pass
    @abc.abstractmethod
    def read(self):
        pass
    
class GSC01(SerialController):
    """Class for the GSC-01 Controller
    Microcontroller Model: OptoSigma GSC-01
    
    Currently the device is to CENTRAL HOME, i.e. the origin is the center of the stage.
    """
    
    # SGSP26-200 : Travel Range 200mm

    # Additional Settings:
    # - Baudrate: 9600
    # - Default Speed:      Min Freq: 500  pps
    # 					    Max Freq: 5000 pps
    # 					    Acceleration: 200 ms
    # - Jog Speed: 500 pps
    # - Run Current: 350 mA
    # - Stop Current 175 mA
    # Set using the GSC-01 Configuration App

    # We always use the axis 1 instead of W

    def __init__(self, stage: Stg.GSC01_Stage = Stg.SGSP26_200(), *args, **kwargs):
        """Constructor

        Parameters
        ----------
        stage : stage._stage.GSC01_Stage
            A stage instance with the correct boundary values set, by default stage._stage.SGSP26_200()

        """
    
        super().__init__(implementation = True, *args, **kwargs)

        self.ENTER = b'\x0D\x0A' # CRLF
        
        self.waitClear() # To make sure controller is on

        # When the Stage is started, the current position is taken as 0
        # For meaningful positioning, we need to home the stage.

        self.stage          = stage
        self.stage.position = self.getPositionReadOut()
        self.axis           = "1"                                    # can take value 1 or W
        
        self._powered = False # Internal management
        self.powered  = True

        # Set speed
        self.initSpeed = {
            "jogSpeed": 500  ,
            "minSpeed": 500  ,
            "maxSpeed": 5000 ,
            "acdcTime": 200 
        }
        self.setSpeed(**self.initSpeed)

        # Check dirtiness
        self.checkDirtiness()
    
    # Init Funcs here
    def checkDirtiness(self):
        try:
            self.safesend(f"M:{self.axis}+P1")
        except stage.errors.ControllerError:
            self.stage.permDirty = True

    # Helper Functions
    # technically works with numpy arrays
    def pulse_to_um(self, pps: int):
        return self.stage.um_per_pulse * pps
    def um_to_pulse(self, um: float, asint: bool = False):
        pps = um / self.stage.um_per_pulse
        return pps if not asint else np.around(pps).astype(int)

    # Property functions here
    @property
    def powered(self):
        return self._powered

    @powered.setter
    def powered(self, state: bool):
        """Sets whether the motor is powered or free spinning.

        Parameters
        ----------
        state : bool
            True for powered, False for not powered

        """

        on = 1 if state else 0

        self.safesend(f"C:{self.axis}{on}")

        if self._powered and not state:
            self.stage.permDirty = True

        self._powered = state
    
    # Implementation Functions here

    @stage.errors.FailWithWarning
    def setSpeed(self, jogSpeed: Optional[int] = None, \
                       minSpeed: Optional[int] = None, \
                       maxSpeed: Optional[int] = None, \
                       acdcTime: Optional[int] = None,
                       init    : Optional[bool]= False):
        """Sets the driving speed of the stage.

        Set speed in units of 100 PPS. Values less than 100 PPS are rounded down.
        If negative values are given, the absolute values will be taken.
        If any illegal values are given, the original values are taken. If this results in maxspeed < minspeed, then they will be switched.

        Initial Values:
        - jogSpeed = 500  PPS (Restart initializes this)
        - minSpeed = 500  PPS 
        - maxSpeed = 5000 PPS 
        - acdcTime = 200  ms

        Parameters
        ----------
        jogSpeed : Optional[int], optional
            The jogging speed of the stage in Pulse Per Seconds, by default None
            If set to None, current speed is used. 
            Acceptables values are 100 - 20000 PPS.
        minSpeed : Optional[int], optional
            The minimum speed of the stage in Pulse Per Seconds, by default None
            If set to None, current speed is used. 
            Acceptables values are 100 - 20000 PPS.
        maxSpeed : Optional[int], optional
            The maximum speed of the stage in Pulse Per Seconds, by default None
            If set to None, current speed is used. 
            Acceptables values are 100 - 20000 PPS.
        acdcTime : Optional[int], optional
            The acceleration and deceleration time of the stage in milliseconds, by default None
            Acceptables values are 0 to 1000 ms.
            If set to None, current acceleration and deceleration time is used. 
        init     : Optional[bool], optional
            Resets the speeds to the initial values. If set to True, other parameters are ignored.
            By default False.

        Returns
        -------
        (retSpeed, retJog) : Statuses
            See GSC01.safesend()

        Raises
        ------
        AssertionError
            If `minSpeed` is more than `maxSpeed`, or if `maxSpeed` is 0
        TypeError
            If any of the values are not integers.

        """
        
        if init:
            return self.setSpeed(**self.initSpeed)

        newvals  = [jogSpeed, minSpeed, maxSpeed, acdcTime]
        original = [self.stage.speed.jog, self.stage.speed.min, self.stage.speed.max, self.stage.acdcTime]

        combine  = [abs(h.ensureInt(x)) if x is not None else original[i] for i, x in enumerate(newvals)]

        assert combine[1] <= combine[2], "minSpeed should be <= maxSpeed"

        for i in range(3):
            # Check if values are multiples of 100
            if (combine[i] % 100):
                new = (combine[i] // 100) * 100
                self.log(f"Got {combine[i]}, using {new}", loglevel = logging.WARN)
                combine[i] = new

            # Speed Boundary checks
            if not (100 <= combine[i] <= 20000):
                self.log(f"Illegal value {combine[i]}, using old value {original[i]}", loglevel = logging.WARN)
                combine[i] = original[i]

        # min/max speed check
        combine[1], combine[2] = (combine[1], combine[2]) if (combine[1] <= combine[2]) else (combine[2], combine[1])

        # acdc time boundary checks
        if not (0 <= combine[3] <= 1000):
            self.log(f"Illegal value {combine[3]}, using old value {original[3]}", loglevel = logging.WARN)
            combine[3] = original[3]
    
        keys             = ["jog", "min", "max"]
        self.stage.speed = namedtuple("StageSpeed", keys)(*combine[:3])
        self.stage.acdcTime  = combine[3]

        self.log("Setting speed: Jog = {}, min = {}, max = {}, acdctime = {}".format(*combine), loglevel = logging.INFO)

        a = self.safesend(f"D:{self.axis}S{self.stage.speed.min}F{self.stage.speed.max}R{self.stage.acdcTime}")
        b = self.safesend(f"S:J{self.stage.speed.jog}")

        return a, b
            
    @stage.errors.FailSilently # To be deleted with GUI
    def homeStage(self):
        """Home the stage
        
        Speeds: 
        - minSpeed = 500  PPS 
        - maxSpeed = 5000 PPS 
        - acdcTime = 200  ms
        The above cannot be changed. 
        
        """
        self.log("Homing stage...", end="\r", loglevel = logging.INFO)

        ret = self.safesend(f"H:{self.axis}")
        self.waitClear()

        # We reset dirtiness
        self.stage._permDirty = False 
        self.stage.dirty      = False
        # self.stage.resetStage() Eventuell, 
        # but I don't want to deal with all the cases resulting from resetPositionToZero()

        self.resetPositionToZero()

        self.log("Homing stage...Done", loglevel = logging.INFO)
        
        return ret

    def resetPositionToZero(self):
        currpos = self.stage.position
        self.stage.position = 0
        
        if self.stage.ranged:
            delta = - currpos
            self.stage.setLimits(upper = self.stage.LIMIT_UPPER + delta, lower = self.stage.LIMIT_LOWER + delta)

        return self.safesend(f"R:{self.axis}")
    
    def findRange(self):
        """Find the range of the stage in number of pulses. Updates `self.stage.pulseRange` directly and returns the pulseRange.

        The `self.stage.um_per_pulse` is also recalculated.
        
        Returns
        -------
        `self.stage.pulseRange` : int
            The obtained pulse range.

        """

        self.log("Finding stage range...", end="\r", loglevel = logging.INFO)

        self.stage.pulseRange = 0

        orig_speed = self.stage.speed.jog
        self.setSpeed(jogSpeed = 4000)

        self.jog(positive = True)
        self.waitClear()
        left = self.getPositionReadOut()

        self.jog(positive = False)
        self.waitClear()
        right = self.getPositionReadOut()

        self.stage.pulseRange = abs(left - right) if not self.devMode else 100557
        self.stage.recalculateUmPerPulse()

        self.syncPosition()

        if self.devMode:
            self.stage.setLimits(upper = 50278, lower = -50278)
        else:
            self.stage.setLimits(upper = max(left, right), lower = min(left, right))

        self.stage.ranged = True

        self.setSpeed(jogSpeed = orig_speed)

        self.log("Finding stage range...Done", loglevel = logging.INFO)

        return self.stage.pulseRange    

    @stage.errors.FailWithWarning
    def jog(self, positive: bool = True, secs: Optional[float] = None):
        """Starts the stage jogging. 

        The stage moves continousely at a preset jog speed without acceleration/deceleration until stopped
        Use `self.setspeed(speed, jog = True)` to set the speed. 
        Use `self.stop(emergency = False)` to stop. 

        Parameters
        ----------
        positive : bool, optional
            Whether to move in the positive direction, by default True
        secs : float, optional
            If given, the amount of time in seconds to jog, by default None
            Uses the system time, so not very accurate, use at own risk. 

        Returns
        -------
        ret : Status
            See GSC01.safesend()

        """

        direction = "+" if positive else "-"

        self.safesend(f"J:{self.axis}{direction}")

        ret = self.safesend("G:")
        self.stage.dirty = True

        if secs is not None and secs >= 0:
            time.sleep(secs)
            return self.stop()
        elif secs is not None and secs < 0:
            raise ValueError(f"Jog Time cannot be negative, got {secs}.")
        
        return ret
    
    @stage.errors.FailWithWarning
    def move(self, pos: int):
        """Absolution move to coordinate `pos`

        Parameters
        ----------
        pos : int
            Absolute coordinate to move to (in units of pulses). Positive for moving in the positive direction, and viceversa.

        Returns
        -------
        ret : Status
            See GSC01.safesend()

        Raises
        ------
        stage.errors.PositionOutOfBoundsError
            If proposed move moves stage out of range

        """
        direction = "+" if pos >= 0 else "-"
        
        # Sanity Check, may raise error
        self.stage.position = pos

        self.safesend(f"A:{self.axis}{direction}P{abs(pos)}")
        return self.safesend("G:")

    @stage.errors.FailWithWarning
    def rmove(self, delta: int):
        """Relative move by `delta` pulses

        Parameters
        ----------
        delta : int
            Number of pulses to move. Positive for moving in the positive direction, and viceversa.

        Returns
        -------
        ret : Status
            See GSC01.safesend()

        Raises
        ------
        stage.errors.PositionOutOfBoundsError
            If proposed relative move moves stage out of range

        """
        direction = "+" if delta >= 0 else "-"
        
        # Sanity Check, may raise error
        self.stage.position += delta

        self.safesend(f"M:{self.axis}{direction}P{abs(delta)}")
        return self.safesend("G:")
    
    @stage.errors.FailWithWarning
    def releaseMotor(self):
        self.powered = False
    
    @stage.errors.FailWithWarning
    def powerMotor(self):
        self.powered = True

    @stage.errors.FailWithWarning
    def syncPosition(self):
        """Gets the position from the controller and syncs it to `stage.position`.
        To calibrate in the other direction (using the software as the source), use `self.move`.

        If the stage is powered, also clears the dirty state of the stage. 

        Returns
        -------
        pos: int
            Current Position of the stage

        """

        pos = self.getPositionReadOut()
        try:
            self.stage.position = pos  # Should not raise any error
        except stage.errors.PositionOutOfBoundsError as e:
            if pos < self.stage.LIMIT_LOWER:
                self.stage.LIMIT_LOWER = pos
            elif pos > self.stage.LIMIT_UPPER:
                self.stage.LIMIT_UPPER = pos

            # Perhaps the stage is now dirty?
            self.stage.pulseRange = abs(self.stage.LIMIT_LOWER - self.stage.LIMIT_UPPER)
            self.stage.recalculateUmPerPulse()
            self.syncPosition()

        if self.powered:
            self.stage.dirty = False

        return pos

    @stage.errors.FailWithWarning
    def getPositionReadOut(self):
        """Gets the position from the controller. 
        Only for the first run, defer others to using self.stage.position

        Returns
        -------
        position: integer
            Position in integer

        """
        return int(self.getStatus1()[0])
    
    @stage.errors.FailWithWarning
    def getStatus1(self, *args, **kwargs):
        """Checks Status1

        Returns
        -------
        ret: array of strings
            Coordinate, ACK1, ACK2, ACK3
            - Coordinate: Fixed Length of 10 digits including symbols. Symbols are left-aligned, coord are right aligned, the extra spaces are removed by read
            - ACK1: X = Command Error, K = Command Accepted normally
            - ACK2: L = LS Stop, K = Normal Stop
            - ACK3: B = Busy Status, R = Ready Status
        """
        if self.devMode:
            return "0,K,K,R"

        return self.safesend("Q:", *args, **kwargs).split(b",")

    @stage.errors.FailWithWarning
    def isBusy(self, *args, **kwargs):
        """Gets operating status, labelled as status2 (B = Busy Status, R = Ready Status)

        Returns
        -------
        ret: bool
            True if Busy, False if Ready, None if output is self.read returns None
        """
        if self.devMode:
            return False

        ret = self.safesend("!:", *args, **kwargs)
        if ret == b'R':
            return False
        if ret == b'B':
            return True
        if ret is None:
            return None
        
        raise stage.errors.ControllerError(f"Unknown Controller Error, received {ret}")

    # Primal Functions Below

    def abort(self):
        """Implementation of abort as specified in the parent class"""
        return self.stop(emergency = True)
    
    @stage.errors.FailWithWarning
    def stop(self, emergency: bool = False):
        """Decelerates the stage and stops it

        Parameters
        ----------
        emergency : bool, optional
            Set to True to use immediate stop instead of decelerate and stop, by default False

        """
        if emergency:
            return self.safesend("L:E")

        if self.stage.dirty:
            self.syncPosition()

        return self.safesend(f"L:{self.axis}")

    def closeDevice(self):
        return super().closeDevice()

    def safesend(self, *args, **kwargs):
        if self.devMode:
            return True

        ret = self.send(*args, **kwargs)

        if ret == b'NG':
            raise stage.errors.ControllerError("Controller returned an error")

        return ret
    
    def send(self, cmd: Union[bytearray, str], waitClear: bool = False, raw: bool = False, waitTime: float = 0):
        """Sends a command to the GSC-01 Controller

        Parameters
        ----------
        cmd : Union[bytearray, str]
            If ```raw = True``` then cmd is a ```bytearray``` that is directly sent to the controller.
            Otherwise, cmd is a string command that is encoded into ASCII before being sent to the controller.
            
        waitClear : bool, optional
            [description], by default False
        raw : bool, optional
            Flag for whether the input command is a bytearray or string, by default False
        waitTime : float, optional
            Waiting time in seconds before writing to the device, by default 0.
            Can be used to cool down.

        Returns
        -------
        output : Union[bytearray,int]
            Returns 0 if ```self.devMode = True``` else returns the results from ```self.read()```
        """
        if self.devMode:
            return 0

        # Writes cmd to the serial channel, returns the data as a list
        cmd = cmd.encode("ascii") + self.ENTER if not raw else cmd

        time.sleep(waitTime)

        if waitClear:
            self.waitClear()

        self.dev.write(cmd)

        return self.read()

    def read(self):
        time.sleep(0.05)

        out = b''
        while self.dev.inWaiting() > 0:
            out += self.dev.read(1)

        out = out.strip().split() if len(out) else ''

        out = out[0] if len(out) == 1 else b''.join([x.strip() for x in out])

        return out if len(out) else None

    def waitClear(self):
        """Waits for the device to be ready.

        Returns
        -------
        True
            Returns True once the controller is ready

        Raises
        ------
        RuntimeError
            If the controller does not respond
        """
        # we wait until all commands are done running and the controller is ready
        if self.devMode:
            return True

        timeoutCount = 0
        timeoutLimit = 5
        waitTime = 0
        waitTimeLimit = 0.3
        while True:
            x = self.isBusy(waitTime = waitTime)
            if x is not None and not x:
                break

            if x is None:
                timeoutCount += 1
                if timeoutCount >= timeoutLimit:
                    timeoutCount = 0
                    waitTime += 0.1

                if waitTime >= waitTimeLimit:
                    raise RuntimeError("waitClear timed out, this should not happen. Did you switch on the microcontroller?")

                # We try again but quit if 2nd time still none

            # print("Waiting for stack to clear...", end="\r")
            time.sleep(0.1)
        # print("Waiting for stack to clear...cleared")

        return True
        

if __name__ == '__main__':
    with GSC01(stage = Stg.SGSP26_200(), devMode = False) as m:
        print("with GSC01 as m")
        import code; code.interact(local=locals())

    # exit
    # import argparse

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-H', '--noHome', help="Do not home the stage", action='store_true')
    # parser.add_argument('-A', '--shutterAbsolute', help="Shutter uses absolute servo", action='store_true')
    # args = parser.parse_args()

    # with Micos(noHome = args.noHome, shutterAbsolute = args.shutterAbsolute) as m:
    # 	print("\n\nm = Micos()\n\n")
    # 	# import pdb; pdb.set_trace()
    # 	import code; code.interact(local=locals())