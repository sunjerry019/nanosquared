#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

from qthelpers import moveToCentre

import platform, ctypes

class Stgctrl(QtWidgets.QWidget):
    def __init__(self, *args):
        super().__init__(*args)

        # self.customicon = os.path.join(base_dir, 'icons', 'shutterbtn.svg')

        self.title = 'Stage Control with Camera'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 500
        self.isOpen = False

        self.initUI()

    # def make_widget_from_layou`t(function):
    #     def wrapper(self):
    #         # We create a widget
    #         widget = QtWidgets.QWidget()
    #         # Get the layout
    #         layout = function(self, widget)
    #         # Assign the layout to the widget
    #         widget.setLayout(layout)

    #         return widget

    #     return wrapper

    # @make_widget_from_layout
    def create_stage(self, widget):
        # Create all child elements

        # need to link to stagecontrol to read position of controllers

        # LCDS
        _lcd_label = QtWidgets.QLabel("Current Position")
        _lcd_label.setAlignment(QtCore.Qt.AlignCenter)
        _lcd_label.setMaximumHeight(20)

        self._lcd = QtWidgets.QLCDNumber()
        self._lcd.setDigitCount(8)
        self._lcd.setSmallDecimalPoint(True)
        self._lcd.setMaximumHeight(200)
        self._lcd.setMinimumHeight(150)
        # TODO: Some styling here for the QLCD number

        # BUTTONS
        self._leftArrow  = QtWidgets.QPushButton(u'\u21E6')
        self._rightArrow = QtWidgets.QPushButton(u'\u21E8')
        self._homeBtn    = QtWidgets.QPushButton("Home\nStage")

        self._stage_buttons = [
            self._leftArrow  ,
            self._rightArrow ,
            self._homeBtn    ,
        ]

        for btn in self._stage_buttons:
            btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            btn.setMaximumHeight(150)

        self.arrowFont = QtGui.QFont("Arial", 30)
        self.arrowFont.setBold(True)

        self._leftArrow.setFont(self.arrowFont)
        self._rightArrow.setFont(self.arrowFont)

        # # SETTINGS AND PARAMS
        # _velocity_label = QtWidgets.QLabel("Velocity ({}m/s)".format(self.MICROSYMBOL))
        # _velocity_label.setAlignment(QtCore.Qt.AlignRight)
        # _step_size_label = QtWidgets.QLabel("Step size ({}m)".format(self.MICROSYMBOL))

        # self._SL_velocity = QtWidgets.QLineEdit()
        # self._SL_velocity.setText('100')
        # self._SL_velocity.setValidator(QtGui.QDoubleValidator(0,10000, 12))
        # # _velocity.setFont(QtGui.QFont("Arial",20))

        # self._SL_step_size = QtWidgets.QLineEdit()
        # self._SL_step_size.setText('10')
        # self._SL_step_size.setValidator(QtGui.QDoubleValidator(0.5,10000, 12))
        # # _step_size.setFont(QtGui.QFont("Arial",20))

        # _SL_settings = QtWidgets.QWidget()
        # _SL_settings_layout = QtWidgets.QVBoxLayout()
        # self._SL_invertx_checkbox = QtWidgets.QCheckBox("Invert Horizontal")
        # self._SL_inverty_checkbox = QtWidgets.QCheckBox("Invert Vertical")
        # _SL_settings_layout.addWidget(self._SL_invertx_checkbox)
        # _SL_settings_layout.addWidget(self._SL_inverty_checkbox)
        # _SL_settings.setLayout(_SL_settings_layout)

        # Create the layout with the child elements
        _stage_layout = QtWidgets.QGridLayout()

        # void QGridLayout::addWidget(QWidget *widget, int row, int column, Qt::Alignment alignment = Qt::Alignment())
        # void QGridLayout::addWidget(QWidget *widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())

        # currx, y label
        _stage_layout.addWidget(_lcd_label, 0, 1, 1, 2)

        # _stage_layout.addWidget(self._lcdx, 1, 1, 1, 2)
        # _stage_layout.addWidget(self._lcdy, 1, 3, 1, 2)

        # _stage_layout.addWidget(_lcdx_label, 0, 1, 1, 2)
        # _stage_layout.addWidget(_lcdy_label, 0, 3, 1, 2)

        # _stage_layout.addWidget(_velocity_label, 2, 0)
        # _stage_layout.addWidget(self._SL_velocity, 2, 1, 1, 2)
        # _stage_layout.addWidget(self._SL_step_size, 2, 3, 1, 2)
        # _stage_layout.addWidget(_step_size_label, 2, 5)

        # _stage_layout.addWidget(self._upArrow, 4, 2, 1, 2)
        # _stage_layout.addWidget(self._downArrow, 5, 2, 1, 2)
        # _stage_layout.addWidget(self._leftArrow, 5, 0, 1, 2)
        # _stage_layout.addWidget(self._rightArrow, 5, 4, 1, 2)

        # _stage_layout.addWidget(_SL_settings, 4, 4, 1, 2)

        # _stage_layout.addWidget(self._homeBtn, 4, 0, 1, 2)

        return _stage_layout

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.setWindowIcon(QIcon(self.customicon))

        moveToCentre(self)

        # self.textbox = QLabel(self)
        # self.textbox.setText("HELLO WORLD\n")
        # self.setStyleSheet("QLabel {font-weight: bold; font-size: 18pt; font-family: Roboto, 'Segoe UI'; }")
        # self.textbox.setMaximumHeight(100)
        # # self.textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        # button = QPushButton('LAUNCH\nSEQUENCE', self)
        # button.setToolTip('A single button. Click it maybe?')
        # button.setStyleSheet("QPushButton {background-color: red; color: black; font-weight: bold; font-size: 20pt; font-family: Roboto, 'Segoe UI';}")
        # button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # button.setMaximumHeight(300)
        # button.setMaximumWidth(350)
        # button.clicked.connect(self.on_click)

        # self._layout.addWidget(self.textbox, 0, 0)

        # # https://stackoverflow.com/a/25515321/3211506
        # self.horizontal_wrapper = QWidget()
        # self.horizontal_wrapper_layout = QHBoxLayout()
        # self.horizontal_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        # self.horizontal_wrapper_layout.addStretch(1)
        # self.horizontal_wrapper_layout.addWidget(button)
        # self.horizontal_wrapper_layout.setStretchFactor(button, 3)
        # self.horizontal_wrapper_layout.addStretch(1)
        # self.horizontal_wrapper.setLayout(self.horizontal_wrapper_layout)

        # self._layout.addWidget(self.horizontal_wrapper, 1, 0)


        # # We still set this as this is not default behaviour on Windows
        # self._layout.setAlignment(self.textbox, Qt.AlignCenter)
        # # self._layout.setAlignment(button, Qt.AlignCenter)

        self._layout = self.create_stage()
        self.setLayout(self._layout)

        self.show()

    # @pyqtSlot()
    # def on_click(self):
    #     if self.isOpen:
    #         self.shutter.close()
    #         self.isOpen = False
    #         self.textbox.setText("You closed the shutter\nGood job!!")
    #     else:
    #         self.shutter.open()
    #         self.isOpen = True
    #         self.textbox.setText("You opened the shutter\nWE'RE DOOMED!!")

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
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
