#!/usr/bin/env python3

# Made 2022, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

# Possible Improvements
# - Different fitting methods
# - Provide option to choose which way the beam is coming in
# - Some proper way of breaking operations

import os, sys
import serial.tools.list_ports

import platform, ctypes

from PyQt5 import QtWidgets
from stagecontrolGUI import Stgctrl 

from cli import CLI

CLI.clear_screen()

try:
    import nanosquared
    print("Using pip-installed version (may not be up-to-date).")
    print("If you have recently updated the repository, do `pip install .` to update the installed version with the one in the repository.")
    print("Otherwise it is safe to ignore this message. ")
except ModuleNotFoundError as e:
    base_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))
    sys.path.insert(0, root_dir)

    import nanosquared

# https://asciiflow.com/

def setup():
    while True:
        print(f"{CLI.COLORS.HEADER}==== SETUP ===={CLI.COLORS.ENDC}")
        print("\nIn the following questions, pressing Enter will enter the default option, which is indicated in capital letters.")
        print("\nIn development mode, no actual devices are required.\nAll function calls will therefore be simulated.")
        print("Use this mode if you only want to fit.")
        devMode = CLI.whats_it_gonna_be_boy("Run in development mode?")

        print("\nNanoScan and WinCamD Beam Profilers are supported. \nyes = NanoScan, no = WinCamD")
        useNanoScan = CLI.whats_it_gonna_be_boy("Use NanoScan?", default = 'yes')

        ports = serial.tools.list_ports.comports()

        print("\nAvailable COM Ports")
        available_ports = []
        default_port = None
        for port, desc, hwid in sorted(ports):
            port_num = port[3:]
            available_ports.append(port_num)
            
            if "communication" in desc.lower() or "comm" in desc.lower():
                default_port = port_num

            print("| {}: {} [{}]".format(port, desc, hwid))
        
        if len(available_ports) < 1:
            print("Error: No COM ports available. Exiting...")
            sys.exit()

        if default_port is None:
            default_port = available_ports[0]

        comPort = int(CLI.options("Which COM Port for stage?", options = available_ports, default = default_port))

        print(f"{CLI.COLORS.HEADER}Obtained:\n--- devMode     : {devMode}\n--- Profiler    : {'NanoScan' if useNanoScan else 'WinCamD'}\n--- COM Port    : COM{comPort}{CLI.COLORS.ENDC}")
        confirm = CLI.whats_it_gonna_be_boy(f"Proceed?", default = "yes")

        if confirm:
            break
        CLI.clear_screen()

    return devMode, useNanoScan, comPort

print(f"""
  ┌──────────────────────────────────────┐
  │                                      │
  │   {CLI.COLORS.OKCYAN}Welcome to M² Measurement Wizard{CLI.COLORS.ENDC}   │
  │                                      │
  │      Made 2021-2022, Yudong Sun      │
  │  github.com/sunjerry019/nanosquared  │
  │                                      │
  └──────────────────────────────────────┘

  - Hint: Control + Z during input exits program.

""")

devMode, useNanoScan, comPort = setup()

cfg = { "port" : f"COM{comPort}" }

cam = nanosquared.cameras.nanoscan.NanoScan if useNanoScan else nanosquared.cameras.wincamd.WinCamD

print(f"{CLI.COLORS.OKGREEN}Got it! Initialising...{CLI.COLORS.ENDC}")
with cam(devMode = devMode) as n:
    with nanosquared.stage.controller.GSC01(devMode = devMode, devConfig = cfg) as s:
        with nanosquared.measurement.measure.Measurement(devMode = devMode, camera = n, controller = s) as M:
            if useNanoScan == True:
                # We implement for NanoScan first
                # https://stackoverflow.com/a/1857/3211506
                # Windows = Windows, Linux = Linux, Mac = Darwin
                # For setting icon on Windows
                if platform.system() == "Windows":
                    # https://stackoverflow.com/a/1552105/3211506
                    myappid = u'MPQ.LEX.GSC01.StageControl' # arbitrary string
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

                APP     = QtWidgets.QApplication(sys.argv)
                STGCTRL = Stgctrl(measurement = M)

            print(f"{CLI.COLORS.OKGREEN}Initialisation done!{CLI.COLORS.ENDC}")

            print("")
            CLI.print_sep()
            print(f"{CLI.COLORS.FAIL}IMPT{CLI.COLORS.ENDC}\n{CLI.COLORS.FAIL}IMPT{CLI.COLORS.ENDC}: If you happen to quit halfway through, use the Task Manager > Processes to ensure that no NanoScanII.exe instances are running before restarting this wizard.\n{CLI.COLORS.FAIL}IMPT{CLI.COLORS.ENDC}: Pressing Ctrl+Z then Enter during input will exit program cleanly.\n{CLI.COLORS.FAIL}IMPT{CLI.COLORS.ENDC}")
            CLI.print_sep()
            print("")
            
            ic = CLI.whats_it_gonna_be_boy("Launch Interactive Console?")

            def launchInteractive(locs):
                CLI.print_sep()
                print(f"\n{CLI.COLORS.OKCYAN}with nanosquared.measurement.measure.Measurement(devMode = {devMode}) as M{CLI.COLORS.ENDC}")
                import code;
                code.interact(local=dict(globals(), **locals(), **locs))

            def launchGUI(_stgctrl, _app):
                print(f"\n{CLI.COLORS.OKCYAN}Close Stage Control GUI to continue{CLI.COLORS.ENDC}\n")
                _stgctrl.measurement.camera.NS.SetShowWindow(True)
                _stgctrl.show()
                _stgctrl.raise_()
                _app.exec_()
                _stgctrl.measurement.camera.NS.SetShowWindow(False)
            
            if ic:
                launchInteractive(locals())
            else:
                if not devMode:
                    if useNanoScan:
                        print(f"You can use the stage control GUI to check your beam parameters (e.g. to see if there are huge variations in data returned)")
                        print(f"// If you want to check the variations, use the GetD4Sigma button.")
                        gui = CLI.whats_it_gonna_be_boy("Launch Stage Control GUI?")
                        if gui:
                            launchGUI(STGCTRL, APP)

                    print("Assuming you want to take a measurement...")
                    while True:
                        while True:
                            wavelength = CLI.getPositiveNonZeroFloat("Laser Wavelength (nm) ?")
                            precision  = CLI.getIntWithLimit("Precision of search? (pulses) ?", default = 10, lowerlimit = 2)

                            if useNanoScan:
                                print(f"NanoScan has the following rotation frequencies (Hz): {n.allowedRots}")
                                scanrate = float(CLI.options("Rotation Frequency of NanoScan?", options = n.allowedRots, default = n.rotationFrequency))

                                print(f"For NanoScan, post processing of raw data before taking a summary is supported.\nYou can use this if you see large variations in the data obtained.\n!! USE WITH CAUTION !!\n\nThe modes are as follows:")
                                print(f"\t0 = Do nothing, use all data to calculate avg and stddev")
                                print(f"\t1 = Remove highest 10% of results before calculating")
                                print(f"\t2 = Remove positive peaks from result based on a threshold")
                                removeOutliers = int(CLI.options("Post processing mode?", options = [0,1,2], default = M.removeOutliers))

                                if removeOutliers == 2:
                                    print(f"The threshold t is interpreted as such:")
                                    print(f"\t 0 < t <= 1: Percentage of the mean to use as the prominence threshold (e.g. 0.2 := 20% * Mean)")
                                    print(f"\t     t >  1: Absolute prominence threshold")
                                    threshold = CLI.getPositiveNonZeroFloat("Threshold?", default = 0.2)
                            else:
                                removeOutliers = 0
                                threshold = 0.2

                            other      = input(CLI.GAP + "Other metadata (e.g. Lens) > ")

                            if useNanoScan:
                                print(f"{CLI.COLORS.HEADER}Obtained:\n--- Wavelength     : {wavelength} nm\n--- Precision      : {precision} pps\n--- Rotation Rate  : {scanrate} Hz\n--- Other Metadata : {other}{CLI.COLORS.ENDC}")
                            else:
                                print(f"{CLI.COLORS.HEADER}Obtained:\n--- Wavelength     : {wavelength} nm\n--- Precision      : {precision} pps\n--- Other Metadata : {other}{CLI.COLORS.ENDC}")

                            confirm = CLI.whats_it_gonna_be_boy(f"Proceed?", default = "yes")

                            if confirm:
                                break

                        meta = {
                            "Wavelength"      : f"{wavelength} nm",
                            "Precision (pps)" : precision,
                            "Metadata"        : other
                        }
                        if useNanoScan:
                            n.rotationFrequency = scanrate
                            meta["NanoScan Rotation Rate (Hz)"] = scanrate

                        M.take_measurements(precision = precision, metadata = meta, removeOutliers = removeOutliers, threshold = threshold) 
                        
                        print(f"{CLI.COLORS.OKGREEN}Done!{CLI.COLORS.ENDC}")

                        print(f"{CLI.COLORS.OKGREEN}Fitting data (X-Axis)...{CLI.COLORS.ENDC}")
                        res = M.fit_data(axis = M.camera.AXES.X, wavelength = wavelength)
                        print(f"{CLI.COLORS.OKGREEN}=== X-Axis ==={CLI.COLORS.ENDC}")
                        print(f"{CLI.COLORS.OKGREEN}=== Fit Result{CLI.COLORS.ENDC}: {res}")
                        print(f"{CLI.COLORS.OKGREEN}=== M-squared{CLI.COLORS.ENDC} : {M.fitter.m_squared}")
                        fig, ax = M.fitter.getPlotOfFit()
                        fig.show()

                        CLI.presskeycont()
                        
                        print(f"{CLI.COLORS.OKGREEN}Fitting data (Y-Axis)...{CLI.COLORS.ENDC}")
                        res = M.fit_data(axis = M.camera.AXES.Y, wavelength = wavelength) # Use defaults (same as above)
                        print(f"{CLI.COLORS.OKGREEN}=== Y-Axis ==={CLI.COLORS.ENDC}")
                        print(f"{CLI.COLORS.OKGREEN}=== Fit Result{CLI.COLORS.ENDC}: {res}")
                        print(f"{CLI.COLORS.OKGREEN}=== M-squared{CLI.COLORS.ENDC} : {M.fitter.m_squared}")
                        fig, ax = M.fitter.getPlotOfFit()
                        fig.show()

                        print(f"{CLI.COLORS.OKGREEN}All Done!{CLI.COLORS.ENDC}")
                        
                        ic2 = CLI.whats_it_gonna_be_boy("Launch Interactive Console?")
                        if ic2:
                            launchInteractive(locals())

                        if useNanoScan:
                            print(f"You can use the stage control GUI to check your beam parameters (e.g. to see if there are huge variations in data returned)")
                            print(f"// If you want to check the variations, use the GetD4Sigma button.")
                            gui = CLI.whats_it_gonna_be_boy("Launch Stage Control GUI?")
                            if gui:
                                launchGUI(STGCTRL, APP)
                        
                        anothermeasurement = CLI.whats_it_gonna_be_boy("Take another measurement?")
                        if not anothermeasurement:
                            break
                else:
                    print("Assuming you want to fit...")
                    while True:
                        while True:
                            wavelength = CLI.getPositiveNonZeroFloat("Laser Wavelength (nm) ?")

                            print(f"{CLI.COLORS.HEADER}Obtained:\n--- Wavelength     : {wavelength} nm{CLI.COLORS.ENDC}")
                            confirm = CLI.whats_it_gonna_be_boy(f"Proceed?", default = "yes")

                            if confirm:
                                break

                        while True:
                            try:
                                filename = input(CLI.GAP + "Filename > ")
                                M.read_from_file(filename = filename, raiseError = True)
                                break
                            except OSError as e:
                                print(f"OSError: {e}. Try again.")
                            except EOFError:
                                print("Encountered EOF, exiting...")
                                sys.exit()
                        
                        print(f"{CLI.COLORS.OKGREEN}Fitting data (X-Axis)...{CLI.COLORS.ENDC}")
                        res = M.fit_data(axis = M.camera.AXES.X, wavelength = wavelength)
                        print(f"{CLI.COLORS.OKGREEN}=== X-Axis ==={CLI.COLORS.ENDC}")
                        print(f"{CLI.COLORS.OKGREEN}=== Fit Result{CLI.COLORS.ENDC}: {res}")
                        print(f"{CLI.COLORS.OKGREEN}=== M-squared{CLI.COLORS.ENDC} : {M.fitter.m_squared}")
                        fig, ax = M.fitter.getPlotOfFit()
                        fig.show()

                        CLI.presskeycont()
                        
                        print(f"{CLI.COLORS.OKGREEN}Fitting data (Y-Axis)...{CLI.COLORS.ENDC}")
                        res = M.fit_data(axis = M.camera.AXES.Y, wavelength = wavelength) # Use defaults (same as above)
                        print(f"{CLI.COLORS.OKGREEN}=== Y-Axis ==={CLI.COLORS.ENDC}")
                        print(f"{CLI.COLORS.OKGREEN}=== Fit Result{CLI.COLORS.ENDC}: {res}")
                        print(f"{CLI.COLORS.OKGREEN}=== M-squared{CLI.COLORS.ENDC} : {M.fitter.m_squared}")
                        fig, ax = M.fitter.getPlotOfFit()
                        fig.show()
                        

                        print(f"{CLI.COLORS.OKGREEN}All Done!{CLI.COLORS.ENDC}")
                        
                        ic2 = CLI.whats_it_gonna_be_boy("Launch Interactive Console?")
                        if ic2:
                            launchInteractive(locals())
                        
                        anotherfit = CLI.whats_it_gonna_be_boy("Fit another?")
                        if not anotherfit:
                            break