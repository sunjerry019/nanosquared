#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

"""File provides the backend for the GUI. It is meant to combine all the modules together"""

from io import TextIOWrapper
import numbers
import os,sys
import signal
from typing import Optional, Tuple, Union, TextIO
import numpy as np
import scipy

from collections import deque

import tempfile
from pathlib import Path
from datetime import datetime

import scipy

base_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir) 

from cameras.camera  import Camera
from cameras.wincamd import WinCamD
from cameras.nanoscan import NanoScan

from cameras.all_constants import CameraAxes

from stage.controller import Controller, GSC01

from fitting.fitter import MsqFitter, MsqOCFFitter, MsqODRFitter
from fitting.fit_functions import omega_z

import logging
import common.helpers as h

import measurement.errors as me

class Measurement(h.LoggerMixIn):
    def __init__(self, 
            camera: Camera         = None, 
            controller: Controller = None,
            devMode: bool          = True
        ) -> None:
        """Backend to the GUI

        Parameters
        ----------
        camera : cameras.camera.Camera, optional
            Instance of a camera to be used, by default None
            If set to `None`, `WinCamD(devMode = devMode)` is used.
        controller : stage.controller.Controller, optional
            Instance of a `stage-controller` to be used, by default None.
            If set to `None`, `GSC01(devMode = devMode)` is used, which by default uses `stage._stage.SGSP26_200()`
        devMode: bool, optional
            If dev mode is set, all actions are simulated. This is passed on to `controller` if `controller` is set
            to `None`. 

        """

        self.devMode = devMode

        if controller is None:
            controller = GSC01(devMode = devMode)
        
        if camera is None:
            camera = WinCamD(devMode = devMode)
        
        # https://stackoverflow.com/questions/10582774/python-why-can-isinstance-return-false-when-it-should-return-true
        assert isinstance(type(camera), type(Camera)), f"Camera ({camera}) is not recognized"
        assert isinstance(type(controller), type(Controller)), f"Controller ({controller}) is not recognized"

        self.controller = controller
        self.camera     = camera

        self.data   = { self.camera.AXES.X : None, self.camera.AXES.Y : None }
        self.fitter = None

        if not self.devMode:
            self.camera.wait_stable()

        self.controller.homeStage()
        self.controller.findRange()

        self.removeOutliers = 0
        self.threshold      = 0.2     

        self.openedFile = None
        
        self.startSignalHandlers()

    def startSignalHandlers(self):
        """ Starts appropriate signal handlers to handle e.g. keyboard interrupts. 
        Ensures safe exit and disconnecting of controller.
        """
        # https://stackoverflow.com/a/4205386/3211506
        signal.signal(signal.SIGINT, self.KeyboardInterruptHandler)

    def KeyboardInterruptHandler(self, signal, frame):
        """Ensures that any open file is closed on keyboard interrupt
        Handles a SIGINT according to https://docs.python.org/3/library/signal.html#signal.signal.

        Parameters
        ----------
        signal : int
            signal number
        frame : signal Frame object
            Frame objects represent execution frames. They may occur in traceback objects (see below), and are also passed to registered trace functions.
        """

        print("^C Detected: Closing any open file")
        self.closeAnyOpenFile()
        raise KeyboardInterrupt
        # use os._exit(1) to avoid raising any SystemExit exception

    def closeAnyOpenFile(self):
        if isinstance(self.openedFile, TextIOWrapper):
            try:
                self.openedFile.close()
                self.openedFile = None
            except OSError as e:
                pass

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        return self.closeAnyOpenFile()

    def take_measurements(self, axis: Camera.AXES = None, center: int = None, rayleighLength: float = None, precision: int = 100, numsamples: int = 50, writeToFile: Optional[str] = None, metadata: dict = dict(), removeOutliers: int = 0, threshold: float = 0.2, saveRaw: bool = False):
        """Function that takes the necessary measurements for M^2, automatically selects the range based
        on the given Rayleigh Length.

        Minimum Resolution for beam width for WinCamD-IR-BB = ~170 um

        According to ISO 11146-1:2021, we need to take measurements at at least 10 different z positions. Approximately 
        half of the measurements shall be distributed within one Rayleigh length on either side of the beam 
        waist, and approximately half of them shall be distributed beyond two Rayleigh lengths from the beam waist.

        This means, we need the travel range of approximately +- 3 z_0

        Parameters
        ----------
        axis : Camera.AXES, optional
            The axis to take the measurement. If set to None, self.camera.AXES.BOTH is taken. By default, None.
        center : int, optional
            The position of the beam-waist in pulses. When set to None, the code auto finds the center. 
        rayleighLength : float, optional
            Rayleigh Length (z_0) in millimeter. When set to None, the code auto finds the z_R. By default None.

            If axis == self.camera.AXES.BOTH, then rayleighLength should be given as [x, y]
            else, rayleightLength should be as a positive float. 
        precision: int, optional
            Precision to pass to find_center and find_zR_pps
            by default 100
        numsamples : int, optional
            Number of samples to take at each point, by default 50
        writeToFile : Optional[str], optional
            File to write to, if set to None, the data will be written to a temporary file for safety sake.
            If set to anything else, it will raise a warning and no file will be written. 
        metadata : dict, optional
            A dictionary of metadata to write to the file. Will be combined with `default_meta`. 
            Format: ` # [key]: [Value] `
            With `default_meta = { "Rayleigh Length": f"{rayleighLength} mm" }`.
            Values in `default_meta` will be overwritten by entries in this parameter. 
            By default, empty `dict()`
        removeOutliers: int, optional
            See documentation in nanoscan.getAxis_avg_D4Sigma()
            
            By default = 0
        threshold: float, optional
            See documentation in nanoscan.getAxis_avg_D4Sigma()

            By default = 0.2
        saveRaw: bool, optional
            If set to True, writes raw data to a temp file. 

            By default, false
        """

        if removeOutliers not in [0, 1, 2]:
            self.log(f"Invalid removeOutlier mode {removeOutliers}! Using mode 0: do nothing", loglevel = logging.warn)
            removeOutliers = 0 

        if removeOutliers == 2:
            # Check if the threshold is valid:
            if not isinstance(threshold, numbers.Number) or threshold <= 0:
                self.log(f"Invalid threshold {threshold}. Using 0.2.", loglevel = logging.warn)
                threshold = 0.2

        self.removeOutliers = removeOutliers
        self.threshold      = threshold

        if not self.devMode and self.controller.stage.dirty:
            self.controller.homeStage()
        
        if axis is None or not isinstance(axis, self.camera.AXES):
            axis = self.camera.AXES.BOTH
            self.log(f"Defaulting to both axis measurement")

        if saveRaw:
            saveRaw = self.get_raw_file(metadata = metadata)
            self.openedFile = saveRaw
            
        # initialization
        self.data = { self.camera.AXES.X : None, self.camera.AXES.Y : None }

        # find params
        # TODO: CHECK IF CENTER IS CORRECT FOR AXIS CHOSEN
        # TODO: Check if rayleigh length is correct size for axis chosen
        if isinstance(saveRaw, TextIOWrapper):
            saveRaw.write("# === Finding Center ===\n")

        if axis == self.camera.AXES.BOTH:
            _center    = self.find_center_xy(precision = precision, saveRaw = saveRaw)          if center is None else center
        else:
            _center    = np.array([self.find_center(precision = precision, saveRaw = saveRaw)]) if center is None else center

        if rayleighLength is None:
            try:
                if isinstance(saveRaw, TextIOWrapper):
                    saveRaw.write("# === Finding Rayleigh Length ===\n")
                rayleighLength = np.array(self.find_zR_pps(center = _center, axis = axis, precision = precision, saveRaw = saveRaw))
            except me.StageOutOfRangeError as e:
                raise me.ConfigurationError(f"The travel range of the stage does not support the current configuration")
        else:
            rayleighLength = np.around(self.controller.um_to_pulse(um = rayleighLength * 1000)).astype(int)

            if np.shape(_center) != np.shape(rayleighLength):
                rayleighLength = np.broadcast_to(rayleighLength, np.shape(_center))

        _within_points    = np.linspace(start=-rayleighLength, stop=rayleighLength, endpoint = True, num = 10, dtype = np.integer)        
        _without_points_1 = np.linspace(start=2*rayleighLength, stop=3*rayleighLength, endpoint = True, num = 5, dtype = np.integer) 
        _without_points_2 = -_without_points_1

        #                                                                              v the center
        points = np.concatenate([_within_points, _without_points_1, _without_points_2, np.zeros_like(_within_points[0:1])])
        points = points + _center

        # Now we have all the points in a 1D or 2D array depending on number of axes.
        points = np.unique(points.flatten())          # We flatten and get the unique points we need to measure
        points = np.sort(points, kind = 'stable')     # Sort the points

        self.log(points)

        # Check if the rayleigh length fits the stage being used by using the min and max
        if (points[0] < (self.controller.stage.LIMIT_LOWER + 10)) or (points[-1] > (self.controller.stage.LIMIT_UPPER - 10)):
            # Check if it supports asymmetrical
            self.log("Trying asymmetrical...")
            asym_without_points = np.linspace(start=2*rayleighLength, stop=3*rayleighLength, endpoint = True, num = 10, dtype = np.integer) 
            
            points = np.concatenate([_within_points, asym_without_points, np.zeros_like(_within_points[0:1])])
            points = points + _center

            points = np.unique(points.flatten())
            points = np.sort(points, kind = 'stable')

            if (points[0] < (self.controller.stage.LIMIT_LOWER + 10)) or (points[-1] > (self.controller.stage.LIMIT_UPPER - 10)):
                self.log("Trying inverted asymmetrical...")
                # We try inverting the points
                points = np.flip(-points)

            if (points[0] < (self.controller.stage.LIMIT_LOWER + 10)) or (points[-1] > (self.controller.stage.LIMIT_UPPER - 10)):
                # if that still doesnt work
                raise me.ConfigurationError(f"The travel range of the stage does not support the current configuration: Travel Range = [{self.controller.stage.LIMIT_LOWER}, {self.controller.stage.LIMIT_UPPER}], Points = [{points[0]}, {points[-1]}]")   
                
        self.log(points)

        totalpts = len(points)
        digits   = len(str(totalpts))

        # Take the measurements
        for n, pt in enumerate(points):
            # https://stackoverflow.com/a/25293744
            self.log(f"Point [{(n+1): >{digits}}/{totalpts}]: {pt}")

            (y_x, y_y) = self.measure_at(pos = pt, numsamples = numsamples, axis = self.camera.AXES.BOTH, saveRaw = saveRaw)
            x = self.controller.pulse_to_um(pps = pt) / 1000 # Convert to mm

            dtpt_x = np.array([x, y_x[0], y_x[1]])
            dtpt_y = np.array([x, y_y[0], y_y[1]])

            self.data[self.camera.AXES.X] = dtpt_x if self.data[self.camera.AXES.X] is None else np.vstack((self.data[self.camera.AXES.X], dtpt_x))
            self.data[self.camera.AXES.Y] = dtpt_y if self.data[self.camera.AXES.Y] is None else np.vstack((self.data[self.camera.AXES.Y], dtpt_y))
            
            # for ax in [self.camera.AXES.X, self.camera.AXES.Y]:
            #     y = self.measure_at(pos = pt, numsamples = numsamples, axis = ax)

        # self.data has the format
        # self.data = {'x': xdata, 'y': ydata }
        # where {x,y}data is an nparray with each element the format [z, diam, delta_diam]

        if isinstance(saveRaw, TextIOWrapper):
            saveRaw.close()
            self.openedFile = None

        default_meta = {
            "Rayleigh Length": f"{self.controller.pulse_to_um(pps = rayleighLength) / 1000} mm"
        }

        metadata = {**default_meta, **metadata}

        if isinstance(saveRaw, TextIOWrapper):
            metadata["Raw Data File"] = os.path.realpath(saveRaw.name)
        
        if isinstance(self.camera, NanoScan):
            postProcMethod = ["0: Do Nothing", "1: Remove top 10%", "2: Remove positive peaks from data"]
            metadata["Post Processing Mode"] = postProcMethod[removeOutliers]
            if removeOutliers == 2:
                metadata["Threshold"] = threshold

        self.write_to_file(writeToFile = writeToFile, metadata = metadata)

        return self.data

    def get_raw_file(self, writeToFile: Optional[str] = None, metadata: Optional[dict] = None) -> TextIO:
        f = None
        pfad = writeToFile

        now = datetime.now()

        if pfad is not None and isinstance(pfad, str):
            # We use the given file
            try:
                f = open(pfad, 'w')
            except OSError as e:
                self.log(f"{pfad}: OSError {e}", logging.ERROR)
        elif pfad is None:
            # We create a file in the M2 directory to save the data.

            tempdir = os.path.join(root_dir, ".." ,"nanosquared-data", "M2")
            Path(tempdir).mkdir(parents=True, exist_ok=True)
            fd, pfad = tempfile.mkstemp(suffix = ".raw.log" if not self.devMode else ".dev.raw.log", prefix = now.strftime("%Y-%m-%d_%H%M%S_"), dir = tempdir, text = True)
            # Returns a file descriptor instead of the file

            f = os.fdopen(fd, 'w')
        else:
            self.log(f"Invalid parameter WriteToFile: {writeToFile}. Skipping writing to file.", logging.WARNING)

            return None
        
        self.log(f"Saving raw data file to {pfad}", logging.INFO)

        f.write(f"# Log started on {now.strftime('%Y-%m-%d at %H:%M:%S')}\n")

        if metadata is not None and isinstance(metadata, dict):
            f.write("# ==== Metadata ====\n")
            for key, val in metadata.items():
                f.write(f"#\t{key}: {val}\n")
        elif metadata is not None:
            self.log(f"No metadata written, invalid metadata received: {metadata}", logging.WARN)
        
        f.write("# ====== Data ======\n")

        return f

    def write_to_file(self, writeToFile: Optional[str] = None, metadata: Optional[dict] = None) -> Union[str, None]:
        """Writes `self.data` to a file given by the parameter `writeToFile`.

        Assumes that `self.data` is written by `self.take_measurements()`.

        Parameters
        ----------
        writeToFile : Optional[str], optional
            The filepath to write to, by default None
            If set to `None`, a temporary file is generated in `{ROOT}/data/local/`
        metadata : Optional[dict], optional
            A dictionary of metadata to write to the file in the format:
            ``` # [key]: [Value] ```
            If set to `None`, no metadata will be written.

        Returns
        -------
        pfad : Union[str,None]
            Returns either the file that has been written to, or None if no file was written.

        """
        f = None
        pfad = writeToFile

        now = datetime.now()

        if pfad is not None and isinstance(pfad, str):
            # We use the given file
            try:
                f = open(pfad, 'w')
            except OSError as e:
                self.log(f"{pfad}: OSError {e}", logging.ERROR)
        elif pfad is None:
            # We create a file in the M2 directory to save the data.

            tempdir = os.path.join(root_dir, ".." ,"nanosquared-data", "M2")
            Path(tempdir).mkdir(parents=True, exist_ok=True)
            fd, pfad = tempfile.mkstemp(suffix = ".dat" if not self.devMode else ".dev.dat", prefix = now.strftime("%Y-%m-%d_%H%M%S_"), dir = tempdir, text = True)
            # Returns a file descriptor instead of the file

            f = os.fdopen(fd, 'w')
        else:
            self.log(f"Invalid parameter WriteToFile: {writeToFile}. Skipping writing to file.", logging.WARNING)

            return None
        
        self.log(f"Using {pfad}", logging.INFO)

        f.write(f"# Data written on {now.strftime('%Y-%m-%d at %H:%M:%S')}\n")

        if metadata is not None and isinstance(metadata, dict):
            f.write("# ==== Metadata ====\n")
            for key, val in metadata.items():
                f.write(f"#\t{key}: {val}\n")
        elif metadata is not None:
            self.log(f"No metadata written, invalid metadata received: {metadata}", logging.WARN)
        
        f.write("# ====== Data ======\n")
        # NOT SAFE BUT
        # We assume that the x and y axis have the same number of datapoints, with same z-coordinates
        if self.data[self.camera.AXES.X].shape == self.data[self.camera.AXES.Y].shape:
            f.write(f"# position[mm]\tx_diam[um]\tdx_diam[um]\ty_diam[um]\tdy_diam[um]\n")
            for i in range(self.data[self.camera.AXES.X].shape[0]):
                f.write(f"{self.data[self.camera.AXES.X][i][0]}\t")
                f.write(f"{self.data[self.camera.AXES.X][i][1]}\t{self.data[self.camera.AXES.X][i][2]}\t")
                f.write(f"{self.data[self.camera.AXES.Y][i][1]}\t{self.data[self.camera.AXES.Y][i][2]}\n")

        f.close()

        self.log(f"Data written to {pfad}", logging.INFO)

        return pfad

    def read_from_file(self, filename: str, raiseError = False):
        """Read from a file written by `self.write_to_file()`

        Parameters
        ----------
        filename : str
            File to read from
        """
        try:
            f = open(filename, 'r')
        except OSError as e:
            self.log(f"Unable to read file: {filename}: OSError {e}", logging.WARN)
            if raiseError:
                raise OSError(e)
            return 
        
        # We assume the format position[mm] x_diam[um] dx_diam[um] y_diam[um] dy_diam[um]
        for line in f:
            l = line.strip()
            if l[0] != "#":
                pos, x_diam, dx_diam, y_diam, dy_diam = [ float(x) for x in l.split("\t") ]
                
                omega   = { self.camera.AXES.X : x_diam,  self.camera.AXES.Y: y_diam  }
                d_omega = { self.camera.AXES.X : dx_diam, self.camera.AXES.Y: dy_diam }

                for ax in [self.camera.AXES.X, self.camera.AXES.Y]:
                    dtpt = np.array([pos, omega[ax], d_omega[ax]])
                    if self.data[ax] is None:
                        self.data[ax] = dtpt
                    else:
                        self.data[ax] = np.vstack((self.data[ax], dtpt))

        f.close()

    def fit_data(self, axis: CameraAxes, wavelength: float, wavelength_error: float = 0, mode: int = MsqFitter.M2_MODE, useODR: bool = False, xerror: float = None) -> np.ndarray:
        """Fits the data as measured by `self.take_measurements()`. Creates a new fitter object every time and overwrites the `self.fitter` object. 

        Parameters
        ----------
        axis : CameraAxes
            Designation according to individual camera
        wavelength : float
            Wavelength to be used, in nm
        wavelength_error : float
            Error of the wavelength to be taken into account. Only taken into account for M2LAMBDA_MODE and ISO_MODE
        mode : int, optional
            Fitting Mode, by default MsqFitter.M2_MODE
        useODR : bool, optional
            Whether to use the ODR fitter instead of `scipy.optimize.curve_fit`, by default False
        xerror: Union[float, array_like], optional
            Error in the z-position in mm. Can also be numpy array with the same size as `self.data[axis][:,0]` i.e. the first column.
            If using ODR, `xerror` needs to be provided. 
            If set to None and `useODR` is set to `True`, `xerror` will be taken as 1 pulse (converted into mm).
            By default None

        Returns 
        -------
        m_squared : array_like of length 2
            np.array([m_squared, m_squared_err]) of floats
            Value of the fitted m_squared and its corresponding error

            Returns [0, 0] upon error.
            
        """
        if self.data[axis] is None:
            self.log("Please measure data before fitting!", logging.ERROR)
            return np.zeros(shape = (2,))

        if not isinstance(axis, self.camera.AXES):
            self.log(f"Unexpected axis {axis}, expected {self.camera.AXES}", logging.ERROR)
            return np.zeros(shape = (2,))

        kwargs = {
            "x"              : self.data[axis][:,0],
            "y"              : self.data[axis][:,1] / 2,
            "yerror"         : self.data[axis][:,2] / 2,
            "wavelength"     : float(wavelength),
            "wavelength_err" : float(wavelength_error),
            "mode"           : mode
        }
        
        if useODR:
            # Ensure xerror is of correct type
            if not isinstance(xerror, (int, float, np.ndarray)):
                self.log(f"Ignoring invalid xerror of type {type(xerror)}: {xerror}", logging.WARN)
                xerror = None
            elif isinstance(xerror, np.ndarray) and self.data[axis][:,0].shape != xerror.shape:
                self.log(f"Ignoring invalid xerror of dimension {xerror.shape}, expected {self.data[axis][:,0].shape}", logging.WARN)
                xerror = None

            kwargs["xerror"] = xerror if xerror is not None else (self.controller.stage.um_per_pulse(1) / 1000)

        self.fitter = MsqODRFitter(**kwargs) if useODR else MsqOCFFitter(**kwargs)
        self.fitter.estimateAndFit()

        return self.fitter.m_squared     

    def find_center(self, axis: CameraAxes = None, precision: int = 100, left: int = None, right: int = None, saveRaw: Optional[TextIO] = None) -> int:
        """Finds the approximate position of the beam waist using ternary search. 
        If `left` or `right` is set to None, the limits of the stage are taken

        Code Reference: https://en.wikipedia.org/wiki/Ternary_search

        Parameters
        ----------
        axis : Optional[CameraAxes]
            Must of the type self.camera.AXES, by default None
            If none, then self.camera.AXES.X is chosen.
        precision : 
            The precision of the center in number of pulses, by default 1000
        left : int, optional
            The smallest possible position, by default None
        right : int, optional
            The biggest possible position, by default None
        saveRaw : TextIO, optional
            See self.measure_at()

            By default, None

        Returns
        -------
        center: int
            The approximate beam-waist position
        """

        if axis is None:
            axis = self.camera.AXES.X

        if not isinstance(axis, self.camera.AXES):
            return None
        
        #### USE XY if XY
        if axis == self.camera.AXES.BOTH:
            return self.find_center_xy(precision = precision, left = left, right = right, saveRaw = saveRaw)
        #################
        
        if self.devMode:
            return self.controller.um_to_pulse(um = (self.SIMULATION_PARAMS["z_0"] * 1000), asint = True)

        if not self.controller.stage.ranged and (left is None or right is None):
            self.controller.findRange()

        if left is None and self.controller.stage.ranged:
            left = self.controller.stage.LIMIT_LOWER
        
        if right is None and self.controller.stage.ranged:
            right = self.controller.stage.LIMIT_UPPER

        absolute_precision = precision

        # We implement the iterative method
        while np.abs(right - left) >= absolute_precision:
            left_third  = np.around(left  + (right - left) / 3).astype(int)
            right_third = np.around(right - (right - left) / 3).astype(int)
            
            l = self.measure_at(axis = axis, pos = left_third, saveRaw = saveRaw)
            r = self.measure_at(axis = axis, pos = right_third, saveRaw = saveRaw)

            # absolute_precision = np.max([l[1], r[1], default_abs_pres])

            if l[0] > r[0]:
                left = left_third
            else:
                right = right_third

        # Left and right are the current bounds; the maximum is between them
        cen = np.around((left + right) / 2).astype(int)
        self.log(f"Center at {cen}")
        return cen

    def find_center_xy(self, precision: int = 100, left: Tuple[int, int] = None, right: Tuple[int, int] = None, saveRaw: Optional[TextIO] = None) -> Tuple[int, int]:
        """Finds the approximate position of the beam waist using ternary search. 
        If `left` or `right` is set to None, the limits of the stage are taken

        Code Reference: https://en.wikipedia.org/wiki/Ternary_search

        Parameters
        ----------
        axis : Optional[CameraAxes]
            Must of the type self.camera.AXES, by default None
            If none, then self.camera.AXES.X is chosen.
        precision : 
            The precision of the center in number of pulses, by default 1000
        left : int, optional
            The smallest possible position, by default None
        right : int, optional
            The biggest possible position, by default None
        saveRaw : TextIO, optional
            See self.measure_at()

            By default, None

        Returns
        -------
        center: int
            The approximate beam-waist position
        """

        # if self.devMode:
        #     return (15, 15)

        if not self.controller.stage.ranged and (left is None or right is None):
            self.controller.findRange()

        if left is None and self.controller.stage.ranged:
            left  = [self.controller.stage.LIMIT_LOWER, self.controller.stage.LIMIT_LOWER]
        
        if right is None and self.controller.stage.ranged:
            right = [self.controller.stage.LIMIT_UPPER, self.controller.stage.LIMIT_UPPER]

        if any(not isinstance(item, int) for item in left) or any(not isinstance(item, int) for item in right):
            self.log(f"Left {left}, Right {right} invalid", logging.WARN)
            return (0, 0)

        if(precision < 2):
            self.log(f"Precision {precision} too small. Ignoring and using precision = 2", logging.WARN)
            precision = 2

        absolute_precision = precision

        # left and right has the format [x, y]
        #                 x, y
        remaining_axes = deque([0, 1])

        self.log(f"L,R: {left}, {right}")

        step = 0

        # We implement the iterative method
        while remaining_axes: # Loop while remaining_axes not empty
            # We first do ternary search on the x-axis, but keep track of the bounds of the y-axis
            # once the x-center is found, it does ternary search on the y-axis using the limits already found

            step += 1
            current_axis = remaining_axes[0] # front of deque is the last element?
            
            one_third   = np.abs(right[current_axis] - left[current_axis]) / 3
            left_third  = np.around(left[current_axis]  + one_third).astype(int)
            right_third = np.around(right[current_axis] - one_third).astype(int)

            self.log(f"[{step}] Axes Remaining : {remaining_axes}: Current: {current_axis},\tLeft: {left},\tRight: {right}", loglevel = logging.DEBUG)
            self.log(f"Search between [{left[current_axis]}, {right[current_axis]}]", loglevel = logging.DEBUG)
            l = self.measure_at(axis = self.camera.AXES.BOTH, pos = left_third, saveRaw = saveRaw)
            self.log(f"=== LEFT  POINT: [{left_third}]\t{l}", loglevel = logging.DEBUG)
            r = self.measure_at(axis = self.camera.AXES.BOTH, pos = right_third, saveRaw = saveRaw)
            self.log(f"=== RIGHT POINT: [{right_third}]\t{r}", loglevel = logging.DEBUG)
            self.log("", loglevel = logging.DEBUG)

            for axis in remaining_axes:
                if l[axis][0] > r[axis][0]:
                    left[axis]  = left_third
                else:
                    # if axis != current_axis and np.abs(l[axis][0] - r[axis][0]) <= np.max(l[axis][1], r[axis][1]):
                    #     # if not the current axis, and l and r are within error of each other, assume there is a problem and we do nothing
                    #     pass
                    # else:
                    #     # Under normal circumstances
                    right[axis] = right_third

            if np.abs(right[current_axis] - left[current_axis]) <= absolute_precision:
                remaining_axes.popleft()
                # we have found that center, remove from the list

        # convert the left and right into numpy arrays
        left  = np.array(left)
        right = np.array(right)
            
        # Left and right are the current bounds; the maximum is between them
        cen = np.around((left + right) / 2).astype(int)
        self.log(f"Center at {cen}")
        return cen

    def find_zR_pps(self, center: int, axis: Camera.AXES, precision: int = 10, other: int = None, kappa1: float = 0, kappa2: float = scipy.constants.golden, saveRaw: Optional[TextIO] = None) -> Union[int, Tuple[int, int]]:
        """Using the center, automatically finds the approximate Rayleigh Length

        IMPORTANT: Assumes that find_center has been run, or that somehow the stage is homed properly

        Parameters
        ----------
        center : int or (int, int)
            The position in pulses of the center of the caustic
        axis : Camera.AXES
            The axis to search for Z_r
        precision: optional, int
            How precise should we be when searching for the z_R. 
            If the precision is too small, the code may never converge.
            By default 10 pps.
        other: optional, int
            Right or leftmost point to search for. If None, prioritizes self.controller.stage.LIMIT_UPPER (searches to the right). 
            If not found, it will try self.controller.stage.LIMIT_LOWER or LIMIT_UPPER depending on the original `other` given.
            By default None.
        kappa1: optional, float
            Should be in the range (0, inf)
            For use in the ITP Method
            By default 0 -> Using the Regula Falsi to find the root
        kappa2: optional, float
            Should be in the range [1, 1+\phi) where \phi is the golden ratio (scipy.constants.golden)
            For use in the ITP Method
            By default scipy.constants.golden
        saveRaw : TextIO, optional
            See self.measure_at()

            By default, None


        Returns
        -------
        rayleighLength : int or (int, int)
            The rayleigh length in pulses
        """

        BOTH = (axis == self.camera.AXES.BOTH)

        if self.devMode:
            sim_zr = self.SIMULATION_PARAMS["z_R"] * 1000
            self.log(f"Simulating Beam with z_R = {self.controller.um_to_pulse(um = sim_zr, asint = True)}")
            # return (100, 200) if BOTH else 100

        # We first get the beam width at the center
        if BOTH:
            # omega_0 = np.array([
            #         self.measure_at(axis = self.camera.AXES.X, pos = center[0]),
            #         self.measure_at(axis = self.camera.AXES.Y, pos = center[1])
            #     ])
            omega_0 = None
        else:
            omega_0 = np.array(self.measure_at(axis = axis, pos = center, saveRaw = saveRaw))

        if omega_0 is not None:
            sqrt2_omega = np.sqrt(2) * omega_0

        def evaluate(pos: int):
            data = self.measure_at(axis = axis, pos = pos, saveRaw = saveRaw)
            return data - sqrt2_omega if BOTH else (data - sqrt2_omega)[0]

        # We implement the ITP Method and somehow improve it so that it keeps track of the other axis as well
        # https://en.wikipedia.org/wiki/ITP_method#The_method

        # Implement for 1 axis first (x-axis)

        ## TODO Check if the center is the correct size

        result = (None, None) if BOTH else None

        if not BOTH:
            if other is None:
                other = self.controller.stage.LIMIT_UPPER

            # We search from the origin outwards
            origin, bound = center, other
            it = 0
            remaining_tries = 1 # the other direction
            err = ""
            while True:
                it += 1

                # We first search for a point that is positive
                # Search from the origin to the bound
                x = np.around(origin + (bound - origin) / 3).astype(int)
                y = evaluate(pos = x)

                self.log(f"Bounding Search [{it}]: \t[{origin} -> {bound}] \t==> f({x}) = {y}")

                if y > 0:
                    break
                elif y == 0: # unlikely but just in case
                    return x
                else:
                    origin = x

                if np.abs(bound - origin) <= precision:
                    # We have not found it
                    if not err:
                        err += f"Unable to find a point > z_R! Search Range [{origin}, {bound}]"
                    else:
                        err += f" and [{origin}, {bound}]"

                    self.log(err, logging.ERROR)
                    
                    if remaining_tries > 0:
                        remaining_tries -= 1
                        origin = center
                        bound  = self.controller.stage.LIMIT_LOWER if (other > center) else self.controller.stage.LIMIT_UPPER
                    else:
                        raise me.StageOutOfRangeError(err)

            waist = (omega_0 - sqrt2_omega)[0] if not self.devMode else evaluate(center)

            if x > center:
                x_a, y_a = center, waist
                x_b, y_b = x, y
            else:
                x_a, y_a = x, y
                x_b, y_b = center, waist

            self.log(f"Initial Values: f({x_a}) = {y_a}, f({x_b}) = {y_b}")

            kappa_1 = kappa1 # (0, inf)
            kappa_2 = kappa2 # [1, 1+\phi) = [1, 1 + scipy.constants.golden] where \phi = 1/2(1+sqrt(5))
            n_0     = 0 # [0, inf) slack variable 

            n_half = np.ceil(np.log2((x_b - x_a)/(2*precision)))
            self.log(f"nhalf = {n_half}", loglevel = logging.DEBUG)
            n_max  = n_half + n_0
            j = 0

            while(x_b - x_a > 2*precision):
                self.log(f"[{j + 1}]: \tf({x_a}) = {y_a} \t<-->\t f({x_b}) = {y_b}", loglevel = logging.INFO)
                # Calculating Parameters
                x_half = (x_a + x_b) / 2
                r = precision * np.power(2, n_max - j) - ((x_b - x_a) / 2)
                delta = kappa_1*np.power((x_b - x_a), kappa_2)
                self.log(f"\t\t|| Calculating Params: x_half = {x_half}, r = {r}, delta = {delta}", loglevel = logging.DEBUG)

                # 1) Interpolation
                #    Calculate the Regula Falsi
                x_f = (y_b*x_a - y_a*x_b)/(y_b - y_a) 
                self.log(f"\t\t|| falsi = {x_f}", loglevel = logging.DEBUG)

                # 2) Truncation
                #    Perturb the estimator x_t towards x_half 
                #    (but maximally to x_half)
                distance = x_half - x_f
                sigma    = np.sign(distance)
                x_t      = x_f + sigma*delta if delta <= np.abs(distance) else x_half
                self.log(f"\t\t|| sigma = {sigma}, x_t = {x_t}", loglevel = logging.DEBUG)

                # Alternativ:
                #    delta = np.min([delta, np.abs(distance)])
                #    x_t = x_f + sigma*delta

                # 3) Projection
                #    Project the estimator to minmax interval (?)
                distance = x_t    - x_half 
                x_itp    = x_half - sigma*r if r < np.abs(distance) else x_t
                self.log(f"\t\t|| x_itp = {x_itp}", loglevel = logging.DEBUG)
                # Alternativ:
                #    r = np.min([r, distance])
                #    x_itp = x_half - sigma*r

                x_itp = np.around(x_itp).astype(int)

                # 4) Updating Interval
                y_itp = evaluate(pos = x_itp)
                orientation = np.sign(y_b - y_a)
                if y_itp * orientation > 0:
                    x_b = x_itp; y_b = y_itp
                elif y_itp * orientation < 0: 
                    x_a = x_itp; y_a = y_itp
                else:
                    # Unlikely but alright
                    x_a = x_itp; x_b = x_itp
                j += 1

            result = np.around((x_a + x_b)/2).astype(int)

        if BOTH:
            # Dirty way: we just run this function twice
            x_axis = self.find_zR_pps(center = center[0], axis = self.camera.AXES.X, precision = precision)
            y_axis = self.find_zR_pps(center = center[1], axis = self.camera.AXES.Y, precision = precision)
            self.log(f"BOTH: X-Axis {x_axis}, Y-axis {y_axis}")
            
            center = np.array(center)
            result = np.array([x_axis, y_axis])

        try:
            if not BOTH: 
                # Since for BOTH, we already have the correct z_R and not the position
                z_R = np.abs(result - center)

            self.log(f"z_R = {self.controller.pulse_to_um(z_R)/1000} mm")
        except Exception as e:
            # When result == None
            z_R = result

        return z_R
        
    def measure_at(self, axis: CameraAxes, pos: int, numsamples: int = 10, removeOutliers: int = None, threshold: float = None, saveRaw: Optional[TextIO] = None):
        """Moves the stage to that position and takes a measurement for the diameter

        If both axis: X: center = 0, Y: center = 100

        Parameters
        ----------
        axis : CameraAxes
            The axis to measure
        pos : int
            Position to measure at in pps
        numsamples: int
            Number of samples to take, by default 10
        removeOutliers: int, optional
            By default, None (i.e. use self.removeOutliers)
        threshold: int, optional
            By default, None (i.e. use self.threshold)
        saveRaw: TextIO
            File to write to. If set to an open file, the raw data will be written to this file.

            Ignored for devMode.

            By default, None.

        Returns
        -------
        d4sigma : Tuple[float, float]
            d4Sigma diameter obtained in the form: [diam, delta diam]
        """
        
        self.controller.move(pos = pos)
        self.controller.waitClear()

        if self.camera.devMode:
            return (self.simulate_beam(pos = pos), self.simulate_beam(pos = (pos - 100))) if axis == self.camera.AXES.BOTH else self.simulate_beam(pos = pos)

        if removeOutliers is None:
            removeOutliers = self.removeOutliers
        
        if threshold is None or threshold < 0:
            threshold = self.threshold

        if isinstance(saveRaw, TextIOWrapper):
            ret, rawout = self.camera.getAxis_avg_D4Sigma(axis, numsamples = numsamples, removeOutliers = removeOutliers, threshold = threshold, returnRaw = True)
            
            position = self.controller.pulse_to_um(pps = pos) / 1000 # Convert to mm
            if axis == self.camera.AXES.BOTH:
                x_axis, y_axis = rawout[:,0], rawout[:,1]
                saveRaw.write(f"# position[mm]\tx_diam[um]\ty_diam[um]\n")
                for i in range(len(x_axis)):
                    saveRaw.write(f"{position}\t{x_axis[i]}\t{y_axis[i]}\n")
            else:
                mapping = {
                    self.camera.AXES.X: "x_diam[um]",
                    self.camera.AXES.Y: "y_diam[um]"
                }
                saveRaw.write(f"# position[mm]\t{mapping[axis]}\n")
                for i in range(len(rawout)):
                    saveRaw.write(f"{position}\t{rawout[i]}\n")

            return ret
        
        return self.camera.getAxis_avg_D4Sigma(axis, numsamples = numsamples, removeOutliers = removeOutliers, threshold = threshold)

    SIMULATION_PARAMS = {
        "z_R"   : 13.65909849, # mm
        "w_0"   : 100        , # um
        "z_0"   : 0          , # mm
        "lambda": 2300         # nm
    }
    def simulate_beam(self, pos: int):
        """Simulates a beam with:
            z_0 = 0 mm, w_0 = 100 um, lambda = 2300 nm
            z_R = 0.013659 m = 13.659 mm = 13659 um

        Parameters
        ----------
        pos : int
            Position

        Returns
        -------
        d4sigma : Tuple[float, float]
            d4Sigma diameter obtained in the form: [diam, delta diam]
        """
        
        # z in mm
        return [2 * omega_z(z = self.controller.pulse_to_um(pos) / 1000, params = [100,0,2300]), 10]
       
    @staticmethod
    def get_w0_zR(diamAtLens: float, focalLength: float, wavelength: float, M2: float = 1) -> Tuple[float, float]:
        """Returns the beam waist radius and the Rayleigh length. 

        Parameters
        ----------
        diamAtLens : float
            Diameter of the beam at the lens in millimeter
        focalLength : float
            Focal length of the lens in millimeter
        wavelength : float
            Wavelength of the laser light in nanometer
        M2 : float, optional
            Estimated M^2 of the beam, by default 1

        Returns
        -------
        w0, zR : Tuple[float, float]
            Tuple with the beam waist radius and the Rayleigh length.
        """
        w0 = Measurement.beam_waist_radius(diamAtLens, focalLength, wavelength, M2)
        zR = Measurement.rayleigh_length(w0, wavelength, M2)

        return (w0, zR)

    @staticmethod
    def rayleigh_length(waistRadius: float, wavelength: float, M2: float = 1) -> float:
        """Calculates the Rayleigh leight given the following parameters

        Reference: https://www.rp-photonics.com/rayleigh_length.html

        Parameters
        ----------
        waistRadius : float
            Beam waist radius in um.
        wavelength : float
            Wavelength of the light used in nm.
        M2 : float, optional
            Estimated M^2 of the beam, by default 1

        Returns
        -------
        rayleigh_length : float
            The Rayleigh length in mm

        """

        return (np.pi * (waistRadius**2)) / wavelength 

    @staticmethod
    def beam_waist_radius(diamAtLens: float, focalLength: float, wavelength: float, M2: float = 1) -> float:
        """Calculates the beam waist radius given the following parameters.

        Reference: https://www.lasercalculator.com/laser-spot-size-calculator/

        Parameters
        ----------
        diamAtLens : float
            Diameter of the beam at the lens in millimeter
        focalLength : float
            Focal length of the lens in millimeter
        wavelength : float
            Wavelength of the laser light in nanometer
        M2 : float, optional
            Estimated M^2 of the beam, by default 1

        Returns
        -------
        beam_waist_radius : float
            The radius of the beam waist in micrometer

        """
        
        beam_waist_radius = (2 * M2 * wavelength * focalLength) / (np.pi * diamAtLens) 

        return beam_waist_radius / 1000

if __name__ == '__main__':
    with Measurement(devMode = True) as M:
        print("with Measurement() as M")
        import code; code.interact(local=locals())
    

    