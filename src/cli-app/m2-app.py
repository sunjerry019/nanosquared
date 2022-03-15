#!/usr/bin/env python3

# Made 2022, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

# Possible Improvements
# - Different fitting methods
# - Provide option to choose which way the beam is coming in
# - Some proper way of breaking operations

from email.policy import default
import os, sys
from matplotlib.style import available
import serial.tools.list_ports

from cli import CLI

try:
    import nanosquared
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

CLI.clear_screen()
print(f"""
  ┌──────────────────────────────────────┐
  │                                      │
  │   {CLI.COLORS.OKCYAN}Welcome to M² Measurement Wizard{CLI.COLORS.ENDC}   │
  │                                      │
  │      Made 2021-2022, Yudong Sun      │
  │  github.com/sunjerry019/nanosquared  │
  │                                      │
  └──────────────────────────────────────┘
""")

devMode, useNanoScan, comPort = setup()

cfg = { "port" : f"COM{comPort}" }

cam = nanosquared.cameras.nanoscan.NanoScan if useNanoScan else nanosquared.cameras.wincamd.WinCamD

print(f"{CLI.COLORS.OKGREEN}Got it! Initialising...{CLI.COLORS.ENDC}")
with cam(devMode = devMode) as n:
    with nanosquared.stage.controller.GSC01(devMode = devMode, devConfig = cfg) as s:
        with nanosquared.measurement.measure.Measurement(devMode = devMode, camera = n, controller = s) as M:
            print(f"{CLI.COLORS.OKGREEN}Initialisation done!{CLI.COLORS.ENDC}")

            print("")
            CLI.print_sep()
            print(f"{CLI.COLORS.FAIL}IMPT{CLI.COLORS.ENDC}\n{CLI.COLORS.FAIL}IMPT{CLI.COLORS.ENDC}: If you happen to quit halfway through, use the Task Manager > Processes to ensure that no NanoScanII.exe instances are running before restarting this wizard.\n{CLI.COLORS.FAIL}IMPT{CLI.COLORS.ENDC}")
            CLI.print_sep()
            print("")
            
            ic = CLI.whats_it_gonna_be_boy("Launch Interactive Console?")

            def launchInteractive():
                CLI.print_sep()
                print(f"\n{CLI.COLORS.OKCYAN}with nanosquared.measurement.measure.Measurement(devMode = {devMode}) as M{CLI.COLORS.ENDC}")
                import code; code.interact(local=locals())
            
            if ic:
                launchInteractive()
            else:
                if not devMode:
                    print("Assuming you want to take a measurement...")
                    while True:
                        while True:
                            wavelength = CLI.getPositiveNonZeroFloat("Laser Wavelength (nm) ?")
                            precision  = CLI.getIntWithLimit("Precision of search? (pulses) ?", default = 10, lowerlimit = 2)
                            other      = input(CLI.GAP + "Other metadata > ")

                            print(f"{CLI.COLORS.HEADER}Obtained:\n--- Wavelength     : {wavelength} nm\n--- Precision      : {precision} pps\n--- Other Metadata : {other}{CLI.COLORS.ENDC}")
                            confirm = CLI.whats_it_gonna_be_boy(f"Proceed?", default = "yes")

                            if confirm:
                                break

                        meta = {
                            "Wavelength"      : f"{wavelength} nm",
                            "Precision (pps)" : precision,
                            "Metadata"        : other
                        }
                        M.take_measurements(precision = precision, metadata = meta) 
                        
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
                            launchInteractive()
                        
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
                                M.read_from_file(filename = filename)
                                break
                            except OSError as e:
                                print(f"OSError: {e}. Try again.")
                        
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
                            launchInteractive()
                        
                        anotherfit = CLI.whats_it_gonna_be_boy("Fit another?")
                        if not anotherfit:
                            break