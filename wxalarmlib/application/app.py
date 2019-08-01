# -*- coding: utf-8 -*-

# ---------------------------------------------------------------
# wxalarm.py
#
# Copyright (c) 2019 sanderiana https://github.com/sanderiana
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
# ---------------------------------------------------------------
# Icon made by Freepik from www.flaticon.com
# ---------------------------------------------------------------

import wx
from wxalarmlib import views


class WxAlarmApp(wx.App):
    LOG_PID = 'pid'
    LOG_APP_MODE = 'app'
    LOG_APP_START = 'start'
    LOG_APP_EXIT = 'exit'
    LOG_APP_KEY = 'action'
    LOG_APP_ALARM = 'alarm'
    LOG_APP_WORK = 'work'

    def __init__(self, store):
        wx.App.__init__(self)
        self.store = store

    def ReadAppIcon(self):
        icon = wx.Icon()
        icon_file = self.store.GetConfig().GetIconPath()
        icon_source = wx.Image(icon_file, wx.BITMAP_TYPE_PNG)
        icon.CopyFromBitmap(icon_source.ConvertToBitmap())
        return icon

    def CreateTopWindow(self):
        def close_event(window):
            window.Close()
            exit(0)
        return views.MainView(data_store=self.store, close_event=close_event)

    def StartMain(self):
        # logger
        logger = self.store.GetLogger()

        # start log
        pid = self.store.GetConfig().GetProcessId()
        log_start = {self.LOG_APP_KEY: self.LOG_APP_START, self.LOG_PID: pid}
        logger.writeLog(self.LOG_APP_MODE, log_start)

        # init view
        view = views.AlarmInitView(parent=None, data_store=self.store)
        view.SetIcon(self.store.GetConfig().ReadAppIcon())
        view.ShowModal()

        # main window
        top_window = self.CreateTopWindow()
        self.SetTopWindow(top_window)
        # icon
        icon = self.store.GetConfig().ReadAppIcon()
        top_window.SetIcon(icon)
        # start
        top_window.Show()
        self.MainLoop()

        # exit log
        log_exit = {self.LOG_APP_KEY: self.LOG_APP_EXIT, self.LOG_PID: pid}
        logger.writeLog(self.LOG_APP_MODE, log_exit)
