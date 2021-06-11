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
sys.path.insert(0, root_dir)

import serial # pyserial
import signal
import json
import warnings
import time

from typing import Union, Optional
import traceback
import platform  	# for auto windows/linux detection
import abc

import stage.errors
from stage._stage import Stage as Stg

class Controller(abc.ABC):
    """Abstract Base Class for a controller"""

    def __init__(self, devMode: bool = True):
        """[summary]

        Parameters
        ----------
        devMode : bool, optional
            To indicate whether to run in developement mode, by default True. 
            When development mode is turned on, no device communication will be started 
        """
        self.devMode = devMode

        self.startSignalHandlers()

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
        print("Shutter will be closed as part of the aborting process.")
        self.abort()
        self.closeDevice()
        print("Exiting")
        sys.exit(1)
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
                warnings.warn("Non-dictionary devConfig. Skipped: {}".format(devConfig))
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
                        warnings.warn("Invalid local config file, not loaded!\n\nError: {}\n\n".format(e))
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
            warnings.warn("devmode -- No serial device will be used")

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

    # Additional Settings:
    # - Baudrate: 9600
    # - Default Speed:      Min Freq: 500  pps
    # 					    Max Freq: 5000 pps
    # 					    Acceleration: 200 ms
    # - Jog Speed: 500 pps
    # - Run Current: 350 mA
    # - Stop Current 175 mA

    # We always use the axis 1 instead of W

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ENTER = b'\x0D\x0A' # CRLF
        self.stage = Stg(pos = self.getPositionReadOut())
        self.axis  = "1"                                    # can take value 1 or W
    
    # Implementation Functions here
     
    @stage.errors.FailSilently # To be deleted with GUI
    def homeStage(self):
        """Home the stage"""
        ret = self.safesend(f"H:{self.axis}")
        self.waitClear()
        self.resetPositionToZero()
        
        return ret

    def resetPositionToZero(self):
        self.stage.position = 0
        return self.safesend(f"R:{self.axis}")

    @stage.errors.FailWithWarning
    def move(self, pos: int):
        """Absolution move to coordinate `pos``

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
            Coordinate: Fixed Length of 10 digits including symbols. Symbols are left-aligned, coord are right aligned
                -> The extra spaces are removed by read
            ACK1: X = Command Error, K = Command Accepted normally
            ACK2: L = LS Stop, K = Normal Stop
            ACK3: B = Busy Status, R = Ready Status
        """

        return self.safesend("Q:", *args, **kwargs).split(b",")

    @stage.errors.FailWithWarning
    def isBusy(self, *args, **kwargs):
        """Gets operating status, labelled as status2 (B = Busy Status, R = Ready Status)

        Returns
        -------
        ret: bool
            True if Busy, False if Ready, None if output is self.read returns None
        """

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

        return self.safesend(f"L:{self.axis}")

    def closeDevice(self):
        if self.dev.isOpen():
            self.dev.close()

    def safesend(self, *args, **kwargs):
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
        # we wait until all commands are done running and the controller is ready
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
    with GSC01(devMode = False) as m:
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