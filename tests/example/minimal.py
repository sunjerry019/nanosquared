from PyQt5 import QtWidgets, QAxContainer
import time

dummyapp = QtWidgets.QApplication([''])
dataCtrl = QAxContainer.QAxWidget("DATARAYOCX.GetDataCtrl.1")
dataCtrl.dynamicCall("StartDriver")                          # Returns True no issues

x = QAxContainer.QAxWidget("DATARAYOCX.ProfilesCtrl.1")

x.setProperty("ProfileID", 22)
dataCtrl.dynamicCall("StartDevice")                          # Returns True
time.sleep(1)
q = dataCtrl.dynamicCall("GetWinCamDataAsVariant")
print(q, len(q))
print(x.dynamicCall("GetProfileDataAsVariant"))              # Always returns 0
dataCtrl.dynamicCall("StopDevice")                           # Always returns False but the light on the camera does turn from red to green