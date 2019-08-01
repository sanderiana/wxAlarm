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


class AlarmModelView(wx.Dialog):
    WINDOW_WIDTH = 370
    WINDOW_HEIGHT = 370

    def __init__(self, parent, data_store, close_event):
        from wxalarmlib.application import WxAlarmDataStore
        self.listItem = {}
        self.title = None
        self.listctrl = None
        self.close_event = close_event
        self.data_store = data_store  # type: WxAlarmDataStore
        self.InitializeComponents(parent)
        self.SetWindowValue()

    def InitializeComponents(self, parent):
        # ------------------------------------------------------------------
        # Layout

        # dialog
        title = "アラーム状態"
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        size = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        wx.Dialog.__init__(self, parent=parent, title=title, size=size, style=style)

        # base layout
        body_panel = wx.Panel(self, wx.ID_ANY)
        contents_vbox = wx.BoxSizer(wx.VERTICAL)
        body_panel.SetSizer(contents_vbox)

        # 1段目
        div1_hbox = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(body_panel, wx.ID_ANY, style=wx.ALIGN_CENTER)
        div1_hbox.Add(title, -1, wx.EXPAND)
        contents_vbox.Add(div1_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 15)
        self.title = title

        # 2段目
        div2_box = wx.BoxSizer(wx.HORIZONTAL)
        listctrl = wx.ListCtrl(body_panel, wx.ID_ANY, style=wx.LC_REPORT)
        div2_box.Add(listctrl, -1, wx.EXPAND)
        contents_vbox.Add(div2_box, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        self.listctrl = listctrl

        # 3段目
        div3_box = wx.BoxSizer(wx.HORIZONTAL)
        button_exit = wx.Button(body_panel,  wx.ID_ANY, "戻る", size=(0, 50))
        div3_box.Add(button_exit, -1, wx.EXPAND)
        contents_vbox.Add(div3_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # ------------------------------------------------------------------
        # ListCtrl

        listctrl.InsertColumn(0, "スケジュール内容", wx.LIST_FORMAT_LEFT, 250)
        listctrl.InsertColumn(1, "状態", wx.LIST_FORMAT_CENTER, 50)
        listctrl.InsertColumn(2, "状態", wx.LIST_FORMAT_CENTER, 50)
        # listctrl.InsertColumn(2, "延長", wx.LIST_FORMAT_CENTER, 50)

        # ------------------------------------------------------------------
        # Event
        button_exit.Bind(wx.EVT_BUTTON, self.OnCloseWindow)
        listctrl.Bind(wx.EVT_LEFT_DCLICK, self.OnItemSelect)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def SetWindowValue(self):
        timer = self.data_store.GetTimerStore()
        alarm_status = timer.GetTodayAlarm()
        title = alarm_status.GetTitle()
        element_dict = alarm_status.GetElementDict()
        self.title.SetLabelText("今日のスケジュール: " + title)
        pos = 0
        for idx, one in element_dict.items():
            title = one.GetStatusText()
            stat = "○" if one.IsEnable() else "-"
            time = one.GetAlarmTime().strftime("%H:%M")
            self.listctrl.InsertItem(pos, title)
            self.listctrl.SetItem(pos, 1, stat)
            self.listctrl.SetItem(pos, 2, time)
            self.listItem[pos] = one
            pos += 1

    def OnItemSelect(self, event):
        def close_event(window):
            window.Close()

        # selected item
        select_index = self.listctrl.GetFirstSelected()
        status_element = self.listItem[select_index]
        if not status_element.IsEnable():
            return

        # view detail view
        from wxalarmlib.views import AlarmChangeView
        view = AlarmChangeView(parent=self, status_element=status_element, close_event=close_event)
        view.ShowModal()
        opt = view.GetSelectOpt()
        if opt is None:
            return

        # change time status
        element = status_element.GetBaseElement()
        timer_store = self.data_store.GetTimerStore()
        current_base = False
        timer_store.AdjustStatus(element, status_element, opt, current_base)

        # reset listctrl
        self.listctrl.DeleteAllItems()
        self.SetWindowValue()

    def OnCloseWindow(self, event):
        self.Unbind(wx.EVT_CLOSE)
        self.close_event(self)
