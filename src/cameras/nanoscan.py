#!/usr/bin/env python3

# Made 2021, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

from PyQt5 import QtWidgets, QAxContainer, QtCore

class NanoScan():
    """Provides interface to the NanoScan 2s Pyro/9/5"""

    def __init__(self, devMode: bool = False, *args, **kwargs):
        self.apertureOpen = False

        self.devMode = devMode

        self.dummyapp = QtWidgets.QApplication([''])

        # Early Binding: NanoScanII.INanoScanII
        # We have to use Late Binding
        self.NS = QAxContainer.QAxObject("photon-nanoscan")  # {FAAD0D22-C718-459A-81CA-268CCF188807}

        numDevices = [-1]
        x = self.NS.dynamicCall("NsAsGetNumDevices(short&)", numDevices) # https://stackoverflow.com/a/25378588
        print(numDevices[0])

        self.NS.dynamicCall("NsAsShowWindow", True)
    
    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        pass

if __name__ == '__main__':
    with NanoScan() as n:
        print("with Nanoscan as n")
        import code; code.interact(local=locals())