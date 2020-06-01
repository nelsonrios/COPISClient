import wx
from ctypes import *
from controller.auiManager import AuiManager
from components.toolBar import ToolBar
from components.menuBar import MenuBar
from components.statusBar import StatusBar

class MyPopupMenu(wx.Menu):
    def __init__(self, parent):
        super(MyPopupMenu, self).__init__()
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.Append(mmi)
        self.Bind(wx.EVT_MENU, self.minimize, mmi)

        cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        self.Append(cmi)
        self.Bind(wx.EVT_MENU, self.close, cmi)

    def minimize(self, e):
        self.parent.Iconize()

    def close(self, e):
        self.parent.Close()
        

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs, style = wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE, title = "COPIS")

        self.cam_list = []
        self.is_edsdk_on = False
        self.edsdkObject = None

        ## set minimum size to show whole interface properly
        self.SetMinSize(wx.Size(1000, 820))

        ## initialize menu bar
        self.SetMenuBar(MenuBar(self))

        ## initialize tool bar
        self.SetToolBar(ToolBar(self))
        self.GetToolBar().Realize()

        ## initialize status bar
        self.SetStatusBar(StatusBar(self))

        ## initialize advanced user interface manager and panes
        self.auiManager = AuiManager(self)
        self.console_panel = self.auiManager.GetPane("Console").window

        self.Centre()
        #self.Bind(wx.EVT_CLOSE, self.quit)


    def quit(self, e):
        self._mgr.UnInit()
        self.Close()

    def rightClick(self, e):
        self.PopupMenu(MyPopupMenu(self), e.GetPosition())

    def initEDSDK(self):
        if self.is_edsdk_on:
            return

        import controller.edsdkObject

        self.edsdkObject = edsdkObject
        self.edsdkObject.initialize(self.console_panel)
        self.is_edsdk_on = True
        self.getCameraList()

    def getCameraList(self):
        self.cam_list = self.edsdkObject.CameraList()
        cam_count = self.cam_list.get_count()

        message = str(cam_count)
        if cam_count == 0:
            message = "There is no camera "

        elif cam_count == 1:
            message += " camera is "
        else:
            message += " cameras are "
        message += "connected."
        
        self.console_panel.print(message)

        for i in range(cam_count):
            canvas = self.auiManager.GetPane('Visualizer').window.onDrawCamera(i)
            self.auiManager.GetPane('Controller').window.masterCombo.Append("camera " + str(i + 1))

    def terminateEDSDK(self):
        if not self.is_edsdk_on:
            return
        
        self.is_edsdk_on = False

        if self.cam_list:
            self.cam_list.terminate()
            self.cam_list = []
