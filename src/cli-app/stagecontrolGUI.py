#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

from qthelpers import moveToCentre

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
        self.height = 200
        self.isOpen = False

        self.initUI()

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

        self._stage_buttons = [
            self._leftArrow  ,
            self._rightArrow ,
            self._homeBtn    ,
            self._d4sigmaBtn
        ]

        for btn in self._stage_buttons:
            btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            btn.setMaximumHeight(150)

        self.arrowFont = QtGui.QFont("Arial", 30)
        self.arrowFont.setBold(True)

        self._leftArrow.setFont(self.arrowFont)
        self._rightArrow.setFont(self.arrowFont)

        # SETTINGS AND PARAMS
        self._numsamples = QtWidgets.QLineEdit()
        self._numsamples.setText('20')
        self._numsamples.setAlignment(QtCore.Qt.AlignCenter)
        self._numsamples.setValidator(QtGui.QIntValidator(1,10000))


        _velocity_label = QtWidgets.QLabel("Jog Speed (pulses/s)")
        _velocity_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        self._velocity = QtWidgets.QLineEdit()
        self._velocity.setText('500')
        self._velocity.setValidator(QtGui.QIntValidator(100,20000))
        self._velocity.setAlignment(QtCore.Qt.AlignCenter)

        # Create the layout with the child elements
        _stage_layout = QtWidgets.QGridLayout()

        # void QGridLayout::addWidget(QWidget *widget, int row, int column, Qt::Alignment alignment = Qt::Alignment())
        # void QGridLayout::addWidget(QWidget *widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())

        # currx, y label
        _stage_layout.addWidget(_lcd_label, 0, 0, 1, 2)
        _stage_layout.addWidget(self._lcd, 1, 0, 4, 2)

        _stage_layout.addWidget(self._leftArrow, 5, 0, 1, 1)
        _stage_layout.addWidget(self._rightArrow, 5, 1, 1, 1)
        _stage_layout.addWidget(self._homeBtn, 6, 0, 1, 2)

        _stage_layout.addWidget(_velocity_label, 1, 3, 1, 1)
        _stage_layout.addWidget(self._velocity, 2, 3, 1, 1)

        _stage_layout.addWidget(_numsamples_label, 3, 3, 1, 1)
        _stage_layout.addWidget(self._numsamples, 4, 3, 1, 1)
        _stage_layout.addWidget(self._d4sigmaBtn, 5, 3, 2, 1)

        return _stage_layout

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setWindowIcon(QIcon(self.customicon))

        moveToCentre(self)

        self._layout = self.create_stage()
        self.setLayout(self._layout)

def main():
    # https://stackoverflow.com/a/1857/3211506
    # Windows = Windows, Linux = Linux, Mac = Darwin
    # For setting icon on Windows
    if platform.system() == "Windows":
        # https://stackoverflow.com/a/1552105/3211506
        myappid = u'MPQ.LEX.GSC01.StageControl' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QtWidgets.QApplication(sys.argv)
    ex = Stgctrl()
    ex.show()
    ex.raise_()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
