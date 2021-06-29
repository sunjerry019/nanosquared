import wx
import wx.lib.activex
import csv
import comtypes.client

class EventSink(object):

    def __init__(self, frame):
        self.counter = 0
        self.frame = frame

    def DataReady(self):
        self.counter +=1
        self.frame.Title= "DataReady fired {0} times".format(self.counter)


class MyApp( wx.App ): 
    
    def OnClick(self,e):
        rb_selection = self.rb.GetStringSelection()
        if rb_selection == "WinCam":
            data = self.gd.ctrl.GetWinCamDataAsVariant()
            data = [[x] for x in data]
        else:
            p_selection = self.cb.GetStringSelection()
            if p_selection == "Profile_X":
                data = self.px.ctrl.GetProfileDataAsVariant()
                data = [[x] for x in data]#csv.writerows accepts a list of rows where each row is a list, a list of lists
            elif p_selection == "Profile_Y":
                data = self.py.ctrl.GetProfileDataAsVariant()
                data = [[x] for x in data]
            else:
                datax = self.px.ctrl.GetProfileDataAsVariant()
                datay = self.py.ctrl.GetProfileDataAsVariant()
                data = [list(row) for row in zip(datax,datay)]#Makes a list of lists; X1 with Y1 in a list, X2 with Y2 in a list etc...
        filename = self.ti.Value
        with open(filename, 'wb') as fp:
            w = csv.writer(fp, delimiter=',')
            w.writerows(data)

    def __init__( self, redirect=False, filename=None ):
        wx.App.__init__( self, redirect, filename )
        self.frame = wx.Frame( parent=None, id=wx.ID_ANY,size=(760,500), title='Python Interface to DataRay')
        #Panel
        p = wx.Panel(self.frame, wx.ID_ANY)
        #Get Data
        self.gd = wx.lib.activex.ActiveXCtrl(p, 'DATARAYOCX.GetDataCtrl.1')
        #The methods of the object are available through the ctrl property of the item
        self.gd.ctrl.StartDriver()
        self.counter = 0
        sink = EventSink(self.frame)
        self.sink = comtypes.client.GetEvents(self.gd.ctrl, sink)
        #Button Panel
        bp = wx.Panel(parent=self.frame, id=wx.ID_ANY, size=(215, 250))
        b1 = wx.lib.activex.ActiveXCtrl(parent=bp,size=(200,50), pos=(7, 0),axID='DATARAYOCX.ButtonCtrl.1')
        b1.ctrl.ButtonID =297 #Id's for some ActiveX controls must be set
        b2 = wx.lib.activex.ActiveXCtrl(parent=bp,size=(100,25), pos=(5, 55),axID='DATARAYOCX.ButtonCtrl.1')
        b2.ctrl.ButtonID =171
        b3 = wx.lib.activex.ActiveXCtrl(parent=bp,size=(100,25), pos=(110,55),axID='DATARAYOCX.ButtonCtrl.1')
        b3.ctrl.ButtonID =172
        b4 = wx.lib.activex.ActiveXCtrl(parent=bp,size=(100,25), pos=(5, 85),axID='DATARAYOCX.ButtonCtrl.1')
        b4.ctrl.ButtonID =177
        b4 = wx.lib.activex.ActiveXCtrl(parent=bp,size=(100,25), pos=(110, 85),axID='DATARAYOCX.ButtonCtrl.1')
        b4.ctrl.ButtonID =179
        #Custom controls
        t = wx.StaticText(bp, label="File:", pos=(5, 115))
        self.ti = wx.TextCtrl(bp, value=r"C:\\Users\\Public\\Documents\\output.csv", pos=(30, 115), size=(170, -1))
        self.rb = wx.RadioBox(bp, label="Data:", pos=(5, 140), choices=["Profile", "WinCam"])
        self.cb = wx.ComboBox(bp, pos=(5,200), choices=[ "Profile_X", "Profile_Y", "Both"])
        self.cb.SetSelection(0)
        myb = wx.Button(bp, label="Write", pos=(5,225))
        myb.Bind(wx.EVT_BUTTON, self.OnClick)
        #Pictures
        pic = wx.lib.activex.ActiveXCtrl(parent=self.frame,size=(250,250),axID='DATARAYOCX.CCDimageCtrl.1')
        tpic = wx.lib.activex.ActiveXCtrl(parent=self.frame,size=(250,250), axID='DATARAYOCX.ThreeDviewCtrl.1')
        palette = wx.lib.activex.ActiveXCtrl(parent=self.frame,size=(10,250), axID='DATARAYOCX.PaletteBarCtrl.1')
        #Profiles
        self.px = wx.lib.activex.ActiveXCtrl(parent=self.frame,size=(300,200),axID='DATARAYOCX.ProfilesCtrl.1')
        self.px.ctrl.ProfileID=22
        self.py = wx.lib.activex.ActiveXCtrl(parent=self.frame,size=(300,200),axID='DATARAYOCX.ProfilesCtrl.1')
        self.py.ctrl.ProfileID = 23
        #Formatting 
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.Add(item=bp,flag=wx.RIGHT, border=10)
        row1.Add(pic)
        row1.Add(item=tpic, flag=wx.LEFT, border=10)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.Add(self.px, 0, wx.RIGHT, 100)# Arguments: item, proportion, flags, border
        row2.Add(self.py)
        col1 = wx.BoxSizer(wx.VERTICAL)
        col1.Add(item=row1, flag=wx.BOTTOM, border=10)
        col1.Add(item=row2, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.frame.SetSizer(col1)
        self.frame.Show()

if __name__ == "__main__":
     app = MyApp()
     app.MainLoop()