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
            ic = CLI.whats_it_gonna_be_boy("Launch Interactive Console?")
            
            if ic:
                CLI.print_sep()
                print(f"\n{CLI.COLORS.OKCYAN}with nanosquared.measurement.measure.Measurement(devMode = {devMode}) as M{CLI.COLORS.ENDC}")
                import code; code.interact(local=locals())
            else:
                if not devMode:
                    while True:
                        meta = {
                            "Wavelength": "2300 nm",
                            "Lens": "f = 250mm CaF2 lens"
                        }
                        M.take_measurements(precision = 10, metadata = meta) 
                        
                        res = M.fit_data(axis = M.camera.AXES.X, wavelength = 2300)
                        print(f"X-Axis")
                        print(f"Fit Result:\t{res}")
                        print(f"M-squared:\t{M.fitter.m_squared}")
                        fig, ax = M.fitter.getPlotOfFit()
                        fig.show()

                        res = M.fit_data(axis = M.camera.AXES.Y, wavelength = 2300) # Use defaults (same as above)
                        print(f"Y-Axis")
                        print(f"Fit Result:\t{res}")
                        print(f"M-squared:\t{M.fitter.m_squared}")
                        fig, ax = M.fitter.getPlotOfFit()
                        fig.show()

                        break
                        # Measurement done, launch interactive?
                        # if not, take another measurement?
                        # no = exit, yes = redo
                else:
                    print("Assuming you want to fit...")




    