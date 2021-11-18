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
        # QAxObject for COM object vs. QAxWidget
        self.NS = QAxContainer.QAxObject("photon-nanoscan")  # {FAAD0D22-C718-459A-81CA-268CCF188807}

    def toggleWindow(self) -> None:
        """Toggles the GUI Window of the NanoScan program"""

        state = self.NS.dynamicCall("NsAsShowWindow")
        self.NS.dynamicCall("NsAsShowWindow", not state)

    def getNumDevices(self) -> int:
        """Gets the number of connected NanoScan devices

        Returns
        -------
        numDevices: int
            Number of NanoScan devices connected.
        """
        numDevices = [-1] # Forces pass-by-reference
        x = self.NS.dynamicCall("NsAsGetNumDevices(short&)", numDevices) # https://stackoverflow.com/a/25378588
        return numDevices[0]
    
    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, traceback):
        pass

if __name__ == '__main__':
    with NanoScan() as n:
        print("with Nanoscan as n")
        import code; code.interact(local=locals())