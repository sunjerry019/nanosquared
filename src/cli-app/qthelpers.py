from PyQt5 import QtWidgets

def moveToCentre(QtObj, host = None):
    # https://stackoverflow.com/a/42326134/3211506
    if host is None:
        host = QtObj.parentWidget()

    if host:
        hostRect = host.frameGeometry()
        QtObj.move(hostRect.center() - QtObj.rect().center())
    else:
        screenGeometry = QtWidgets.QDesktopWidget().availableGeometry()
        try:
            ObjWidth = QtObj.width()
            ObjHeight = QtObj.height()
        except TypeError as e:
            ObjWidth = QtObj.width
            ObjHeight = QtObj.height

        _x = (screenGeometry.width() - ObjWidth) / 2
        _y = (screenGeometry.height() - ObjHeight) / 2
        QtObj.move(_x, _y)