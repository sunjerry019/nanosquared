#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Only works with NanoScan

# Made 2022, Sun Yudong
# yudong.sun [at] mpq.mpg.de / yudong [at] outlook.de

import sys, os
from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtGui import QIcon

from qthelpers import moveToCentre

from nanosquared.cameras.nanoscan import NanoScan
from nanosquared.stage.controller import GSC01
from nanosquared.measurement.measure import Measurement

import platform, ctypes

class Stgctrl(QtWidgets.QWidget):
    def __init__(self, measurement: Measurement, *args): 
        super().__init__(*args)

        self.customicon = os.path.join('logo-plain.svg')

        self.title = 'Stage Control with Camera'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 230

        self.measurement = measurement

        self.initUI()
        self.initEventListeners()

        self.lastSetSpeed = int(self._velocity.text())
        self.measurement.controller.setSpeed(jogSpeed = self.lastSetSpeed)

    def create_stage(self):
        # Create all child elements

        # need to link to stagecontrol to read position of controllers

        # LCD
        _lcd_label = QtWidgets.QLabel("Current Position")
        _lcd_label.setAlignment(QtCore.Qt.AlignCenter)

        self.labelFont = QtGui.QFont("Arial", 24)
        self.labelFont.setBold(True)
        _lcd_label.setFont(self.labelFont)

        self._lcd = QtWidgets.QLCDNumber()
        self._lcd.setDigitCount(10)
        self._lcd.setSmallDecimalPoint(True)
        self._lcd.setMaximumHeight(200)
        self._lcd.setMinimumHeight(100)

        _numsamples_label = QtWidgets.QLabel("Number of Samples")
        _numsamples_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        # BUTTONS
        self._leftArrow  = QtWidgets.QPushButton(u'\u21E6')
        self._rightArrow = QtWidgets.QPushButton(u'\u21E8')
        self._homeBtn    = QtWidgets.QPushButton("Home Stage")
        self._d4sigmaBtn = QtWidgets.QPushButton("Take D4Sigma\nBeam Width\n(Both Axis)")
        self._stopButton = QtWidgets.QPushButton("!<STOP>!")
        self._NSGUIBtn   = QtWidgets.QPushButton("Show/Hide\nNanoScan GUI")

        self._stage_buttons = [
            self._leftArrow  ,
            self._rightArrow ,
            self._homeBtn    ,
            self._d4sigmaBtn ,
            self._stopButton,
            self._NSGUIBtn
        ]

        for btn in self._stage_buttons:
            btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            btn.setMaximumHeight(150)

        self.arrowFont = QtGui.QFont("Arial", 30)
        self.arrowFont.setBold(True)

        self._leftArrow.setFont(self.arrowFont)
        self._rightArrow.setFont(self.arrowFont)
        
        self._stopButton.setStyleSheet("font-weight: bold; background-color: #cb3365; color: #ffffff;")

        # SETTINGS AND PARAMS
        self._numsamples = QtWidgets.QLineEdit()
        self._numsamples.setText('20')
        self._numsamples.setAlignment(QtCore.Qt.AlignCenter)
        self._numsamples.setValidator(QtGui.QIntValidator(1,10000))

        _velocity_label = QtWidgets.QLabel("Jog Speed (pulses/s)")
        _velocity_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        _velocity_warning_label = QtWidgets.QLabel("""Press `STOP` to retrieve position. We recommend speed = 4000 pps. 
Stage might not move when certain speeds are set. In that case, position data will be dirty.
FIX: For each end: Let the stage travel to edge and press `STOP` after the stage has stopped.""")
        _velocity_warning_label.setAlignment(QtCore.Qt.AlignLeft)
        # _velocity_warning_label.setStyleSheet("color: red;")

        self._velocity = QtWidgets.QLineEdit()
        self._velocity.setText('4000')
        self._velocity.setValidator(QtGui.QIntValidator(100,20000))
        self._velocity.setAlignment(QtCore.Qt.AlignCenter)

        if self.measurement is not None:
            self.measurement.controller.setSpeed(jogSpeed = 4000)

        _scan_speed_label = QtWidgets.QLabel("NanoScan Scan Rate (Hz)")
        _scan_speed_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self._scan_speed = QtWidgets.QComboBox()
        if self.measurement is not None:
            for rate in self.measurement.camera.allowedRots:
                self._scan_speed.addItem(str(rate))
            
            index = self.measurement.camera.allowedRots.index(self.measurement.camera.rotationFrequency)
            if index != -1 :
                self._scan_speed.setCurrentIndex(index)
        else:
            for rate in [1.25, 2.5, 5.0, 10.0, 20.0]:
                self._scan_speed.addItem(str(rate))

            self._scan_speed.setCurrentIndex(3)
        
        # Create the layout with the child elements
        _stage_layout = QtWidgets.QGridLayout()

        # void QGridLayout::addWidget(QWidget *widget, int row, int column, Qt::Alignment alignment = Qt::Alignment())
        # void QGridLayout::addWidget(QWidget *widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())

        # currx, y label
        _stage_layout.addWidget(_lcd_label, 0, 0, 1, 2)
        _stage_layout.addWidget(self._lcd, 1, 0, 5, 2)

        _stage_layout.addWidget(self._leftArrow, 6, 0, 1, 1)
        _stage_layout.addWidget(self._rightArrow, 6, 1, 1, 1)
        _stage_layout.addWidget(self._homeBtn, 7, 0, 1, 1)
        _stage_layout.addWidget(self._stopButton, 7, 1, 1, 1)

        _stage_layout.addWidget(_velocity_label, 2, 2, 1, 1)
        _stage_layout.addWidget(self._velocity, 3, 2, 1, 1)

        _stage_layout.addWidget(_numsamples_label, 4, 2, 1, 1)
        _stage_layout.addWidget(self._numsamples, 5, 2, 1, 1)
        _stage_layout.addWidget(self._d4sigmaBtn, 6, 2, 1, 1)
        _stage_layout.addWidget(self._NSGUIBtn, 7, 2, 1, 1)

        _stage_layout.addWidget(_scan_speed_label, 0, 2, 1, 1)
        _stage_layout.addWidget(self._scan_speed, 1, 2, 1, 1)

        _stage_layout.addWidget(_velocity_warning_label, 8, 0, 1, 3)

        return _stage_layout

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setWindowIcon(QIcon(self.customicon))

        moveToCentre(self)

        self._layout = self.create_stage()
        self.setLayout(self._layout)

    def initEventListeners(self):
        self.installEventFilter(self)

        self._homeBtn.clicked.connect(lambda: self.homeStage())

        self._leftArrow.clicked.connect(lambda: self.jog(positive = True))
        self._rightArrow.clicked.connect(lambda: self.jog(positive = False))
        self._stopButton.clicked.connect(lambda: self.stop())

        self._d4sigmaBtn.clicked.connect(lambda: self.measureD4Sigma())

        self._NSGUIBtn.clicked.connect(lambda: self.showHideNSGUI())

        self._scan_speed.currentIndexChanged.connect(lambda: self.changeScanSpeed())
    
    def showHideNSGUI(self):
        if self.measurement is not None:
            if not self.measurement.camera.devMode:
                _guiopen = self.measurement.camera.NS.GetShowWindow()
                self.measurement.camera.NS.SetShowWindow(not _guiopen)

    def homeStage(self):
        if self.measurement is not None:
            self.measurement.controller.homeStage()
            self.resyncPos()

    def changeScanSpeed(self):
        if self.measurement is not None:
            rot = float(self._scan_speed.currentText())
            self.measurement.camera.rotationFrequency = rot

    def measureD4Sigma(self, *args, **kwargs):
        if self.measurement is not None:
            _numSamples = int(self._numsamples.text())
            if _numSamples > 0:
                res = self.measurement.camera.getAxis_avg_D4Sigma(axis = self.measurement.camera.AXES.BOTH, numsamples = _numSamples)
                _x, _y = res[0], res[1]
                self.informationDialog(message = f"X-Axis: {_x}\nY-Axis: {_y}", host = self)
            else:
                self.informationDialog(message = f"Invalid Number of Samples", host = self)

    def informationDialog(self, message, title = "Information", informativeText = None, host = None):
        _msgBox = QtWidgets.QMessageBox(host)
        _msgBox.setIcon(QtWidgets.QMessageBox.Information)
        _msgBox.setWindowTitle(title)
        _msgBox.setText(message)
        if informativeText is not None:
            _msgBox.setInformativeText(informativeText)

        # Get height and width
        _h = _msgBox.height()
        _w = _msgBox.width()
        _msgBox.setGeometry(0, 0, _w, _h)

        moveToCentre(_msgBox)

        _msgBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        ret = _msgBox.exec_()

        return ret

    def jog(self, *args, **kwargs):
        if self.measurement is not None:
            _spd = int(self._velocity.text())
            if _spd != self.lastSetSpeed:
                self.lastSetSpeed = _spd
                self.measurement.controller.setSpeed(jogSpeed = self.lastSetSpeed)

            self.measurement.controller.jog(*args, **kwargs)

    def stop(self, *args, **kwargs):
        if self.measurement is not None:
            self.measurement.controller.stop(*args, **kwargs)
            self.resyncPos()

    def resyncPos(self):
        if self.measurement is not None:
            self.measurement.controller.syncPosition()
            self._lcd.display(self.measurement.controller.stage.position)

    def eventFilter(self, source, evt):
        # https://www.riverbankcomputing.com/static/Docs/PyQt4/qt.html#Key-enum
        # print(evt)

        # https://stackoverflow.com/a/30361237/3211506
        if evt.type() == QtCore.QEvent.ActivationChange:
            if self.isActiveWindow():
                # Focus in
                self.resyncPos()

        if isinstance(evt, QtGui.QKeyEvent): #.type() ==
            # Check source here
            evtkey = evt.key()

            if (evt.type() == QtCore.QEvent.KeyRelease):
                # print("KeyRelease : {}".format(evtkey))

                # All KeyRelease events go here

                if source == self:
                    if evtkey == QtCore.Qt.Key_Left:
                        self.jog(positive = True)

                    if evtkey == QtCore.Qt.Key_Right:
                        self.jog(positive = False)

        # return QtWidgets.QWidget.eventFilter(self, source, evt)
        return super(QtWidgets.QWidget, self).eventFilter(source, evt)

def main():
    # https://stackoverflow.com/a/1857/3211506
    # Windows = Windows, Linux = Linux, Mac = Darwin
    # For setting icon on Windows
    if platform.system() == "Windows":
        # https://stackoverflow.com/a/1552105/3211506
        myappid = u'MPQ.LEX.GSC01.StageControl' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    with NanoScan(devMode = False) as n:
        with GSC01(devMode = True) as s:
            with Measurement(camera = n, controller = s, devMode = True) as m:
                app = QtWidgets.QApplication(sys.argv)
                ex = Stgctrl(measurement = m)
                ex.show()
                ex.raise_()
                ex.setFocus(True)
                sys.exit(app.exec_())

if __name__ == '__main__':
    main()
