#!/usr/bin/env python3

import wx
import wx.lib.activex

# wxpython from conda-forge: conda install -c conda-forge wxpython

class MyApp(wx.App):
    def __init__(self, redirect = False, filename = None, *args, **kwargs):
        super().__init__(redirect=redirect, filename=filename, *args, **kwargs)
        self.frame = wx.Frame(parent = None, id = wx.ID_ANY, size = (500, 500), title = 'Python Interface to Dataray')
        
        # Panel
        p = wx.Panel(self.frame, wx.ID_ANY)

        # Get Data
        self.gd = wx.lib.activex.ActiveXCtrl(p, 'DATARAYOCX.GetDataCtrl.1')
        self.gd.ctrl.StartDriver()

        # Button 
        b1 = wx.lib.activex.ActiveXCtrl(parent = p, size = (100,50), axID = 'DATARAYOCX.ButtonCtrl.1')
        b1.ctrl.ButtonID = 297

        # CCDImage
        wx.lib.activex.ActiveXCtrl(parent = p, size = (250, 250), axID = 'DATARAYOCX.CCDimageCtrl.1')
        wx.lib.activex.ActiveXCtrl(parent = self.frame, size = (10, 250), axID = 'DATARAYOCX.PaletteBarCtrl.1')

        self.frame.Show()


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()