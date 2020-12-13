#!/usr/bin/env python3

# This file is part of COPISClient.
#
# COPISClient is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# COPISClient is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with COPISClient.  If not, see <https://www.gnu.org/licenses/>.

"""Main COPIS App (GUI)."""

import wx
import wx.lib.inspection

import copisconsole
import copiscore
from appconfig import AppConfig
from copiscore import COPISCore
from gui.main_frame import MainWindow

# class COPISWindow(MainWindow, copisconsole.COPISConsole):
#     def __init__(self, *args, **kwargs):
#         copisconsole.COPISConsole.__init__(self)
#         MainWindow.__init__(self, *args, **kwargs)

class COPISApp(wx.App):
    """Main wxPython app.

    Initializes COPISCore and main frame.
    """

    mainwindow = None

    def __init__(self, *args, **kwargs) -> None:
        super(COPISApp, self).__init__(*args, **kwargs)
        self.appconfig = None
        self.appconfig_exists = False
        self.init_appconfig()

        self.locale = wx.Locale(wx.Locale.GetSystemLanguage())
        self.chamberdims = [self.appconfig._device_config.getint('Chamber', 'chamberwidth'),
            self.appconfig._device_config.getint('Chamber', 'chamberdepth'),
            self.appconfig._device_config.getint('Chamber', 'chamberheight'),
            self.appconfig._device_config.getint('Chamber', 'centerwidth'),
            self.appconfig._device_config.getint('Chamber', 'centerdepth'),
            self.appconfig._device_config.getint('Chamber', 'centerheight')]
        self.cam_number = self.appconfig._device_config.getint('Camera', 'camnumber')
        self.cam_x_coords = []
        self.cam_y_coords = []
        self.cam_z_coords = []
        for i in range(1, self.cam_number + 1):
            self.cam_x_coords.extend([self.appconfig._device_config.getint('Camera'+str(i), 'caminitialx')])
            self.cam_y_coords.extend([self.appconfig._device_config.getint('Camera'+str(i), 'caminitialy')])
            self.cam_z_coords.extend([self.appconfig._device_config.getint('Camera'+str(i), 'caminitialz')])
        self.c = COPISCore(self.cam_number, [self.cam_x_coords,
            self.cam_y_coords,
            self.cam_z_coords,
            ]
        )
        self.AppName = 'COPIS Interface'
        self.mainwindow = MainWindow(
            self.chamberdims,
            None,
            style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE,
            title='COPIS',
            size=(self.appconfig._config.getint('General', 'windowwidth'),
                  self.appconfig._config.getint('General', 'windowheight'))
        )
        self.mainwindow.Show()

    def init_appconfig(self) -> None:
        """Init AppConfig."""
        if self.appconfig is None:
            self.appconfig = AppConfig()

        self.appconfig_exists = self.appconfig.exists()
        if self.appconfig_exists:
            self.appconfig.load()


if __name__ == '__main__':
    app = COPISApp()
    try:
        # wx.lib.inspection.InspectionTool().Show() # debug
        app.MainLoop()
    except KeyboardInterrupt:
        pass

    if app.c.edsdk_enabled:
        app.c.terminate_edsdk()
    del app
