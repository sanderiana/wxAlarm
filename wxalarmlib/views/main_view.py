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


class MainView(wx.Frame):
    WINDOW_WIDTH = 270
    WINDOW_HEIGHT = 200

    def __init__(self, data_store, close_event):
        from wxalarmlib.application import WxAlarmDataStore
        self.close_event = close_event
        self.data_store = data_store  # type: WxAlarmDataStore
        self.timer = None
        self.InitializeComponents()

    def Show(self, show=True):
        # self.SelectAlartType()
        super(MainView, self).Show(show)
        self.timer.Start(1000)

    def InitializeComponents(self):
        # ------------------------------------------------------------------
        # Layout
        title = "タイムコーチ"
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        size = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        wx.Frame.__init__(self, parent=None, title=title, size=size, style=style)
        wrap_panel = wx.Panel(self)
        wrap_sizer = wx.GridSizer(1, 1, 0, 0)

        main_panel = wx.Panel(wrap_panel)
        button_open_alarm = wx.Button(main_panel, -1, "アラーム調整")
        button_exit = wx.Button(main_panel, -1, "終了")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button_open_alarm, 1, flag=wx.EXPAND)
        sizer.Add(button_exit, 1, flag=wx.EXPAND)
        main_panel.SetSizer(sizer)

        wrap_sizer.Add(main_panel, flag=wx.EXPAND | wx.ALL, border=10)
        wrap_panel.SetSizer(wrap_sizer)

        # ------------------------------------------------------------------
        # Timer
        self.timer = wx.Timer(self)

        # ------------------------------------------------------------------
        # Event
        button_open_alarm.Bind(wx.EVT_BUTTON, self.OnOpenAlarm)
        button_exit.Bind(wx.EVT_BUTTON, self.OnCloseWindow)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnTimer(self, event):
        timer = self.data_store.GetTimerStore()
        timer.CheckAllStatus(self)

    def OnOpenAlarm(self, event):
        timer = self.data_store.GetTimerStore()
        alarm_status = timer.GetTodayAlarm()
        if alarm_status is None:
            style = wx.OK | wx.ICON_EXCLAMATION
            title = 'エラー'
            message = "起動時にアラームを設定していません"
            dialog = wx.MessageDialog(None, message, title, style=style)
            dialog.ShowModal()
            dialog.Destroy()
            return

        def close_event(window):
            window.Close()
        from wxalarmlib.views import AlarmModelView
        view = AlarmModelView(parent=self, data_store=self.data_store, close_event=close_event)
        view.ShowModal()

    def OnCloseWindow(self, event):
        self.Unbind(wx.EVT_CLOSE)
        self.close_event(self)

