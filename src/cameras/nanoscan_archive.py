# win32com

import win32com

# import nanoscan_activex as NSAx # does not work
import win32com.client as wc

# ui = QtCore.QMetaType(36) # ushort https://doc.qt.io/qt-5/qmetatype.html
# ui = QtCore.QMetaType(31) # voidstar https://doc.qt.io/qt-5/qmetatype.html
# ui = np.array([-1], dtype=np.int16)
# ui = ctypes.c_short(-1)

x = 10
self.NS = wc.Dispatch("photon-nanoscan")
self.NS.NsAsGetNumDevices(ui)
print(ui)