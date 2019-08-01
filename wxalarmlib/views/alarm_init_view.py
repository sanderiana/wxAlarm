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
from wxalarmlib import repository


class AlarmInitView(wx.Dialog):
    WINDOW_WIDTH = 370
    WINDOW_HEIGHT = 370

    def __init__(self, parent, data_store):
        from wxalarmlib.application import WxAlarmDataStore
        self.title = None
        self.listctrl = None
        self.listItem = {}
        self.selected_alarm = None  # type: repository.AlarmElement
        self.data_store = data_store  # type: WxAlarmDataStore
        self.InitializeComponents(parent)

    def GetSelectedAlarm(self):
        return self.selected_alarm

    def ShowModal(self):
        self.SetWindowValue()
        super(AlarmInitView, self).ShowModal()

    def InitializeComponents(self, parent):
        # ------------------------------------------------------------------
        # Layout

        # dialog
        title = "今日のアラーム設定"
        style = wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
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
        button_start = wx.Button(body_panel,  wx.ID_ANY, "開始", size=(0, 50))
        div3_box.Add(button_start, -1, wx.EXPAND)
        contents_vbox.Add(div3_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # ------------------------------------------------------------------
        # ListCtrl

        listctrl.InsertColumn(0, "スケジュール概要", wx.LIST_FORMAT_LEFT, 350)

        # ------------------------------------------------------------------
        # Event
        button_start.Bind(wx.EVT_BUTTON, self.OnStartAlarm)
        listctrl.Bind(wx.EVT_LEFT_DCLICK, self.OnOpenSchedule)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def SetWindowValue(self):
        self.title.SetLabelText("今日のアラームを選択してください")
        data_store = self.data_store
        repo = data_store.GetAlarmRepo()
        dicts = repo.GetListByType(repository.AlarmElement.INI_TYPE_TIME_TABLE)

        order = {}
        for section, element in dicts.items():  # type: str, repository.AlarmElement
            index = int(element.GetByField(repository.AlarmElement.INI_INDEX))
            order[index] = element

        pos = 0
        for index, element in order.items():
            title = element.GetTitle()
            print str(index )+ title

            self.listctrl.InsertItem(pos, title)
            self.listItem[pos] = element
            pos += 1

    def OnOpenSchedule(self, event):
        def close_event(window):
            window.Close()

        # selected item
        select_index = self.listctrl.GetFirstSelected()
        element = self.listItem[select_index]

        # view detail view
        from wxalarmlib.views import AlarmDetailView
        view = AlarmDetailView(parent=self, element=element, close_event=close_event)
        view.ShowModal()

    def OnStartAlarm(self, event):
        # get selected index
        select_index = self.listctrl.GetFirstSelected()
        if select_index == -1:
            style = wx.OK | wx.ICON_EXCLAMATION
            title = '今日のアラーム'
            message = "実行するアラームを選択してください"
            dialog = wx.MessageDialog(None, message, title, style=style)
            dialog.ShowModal()
            dialog.Destroy()
            return

        # selected item
        element = self.listItem[select_index]

        # message box
        style = wx.YES_NO
        title = '今日のアラーム'
        message = "「%s」でアラームを開始しますか？" % element.GetTitle()
        dialog = wx.MessageDialog(None, message, title, style=style)

        # after message
        res = dialog.ShowModal()
        if res == wx.ID_YES:
            timer = self.data_store.GetTimerStore()
            timer.SetTodayAlarm(element)
            self.Unbind(wx.EVT_CLOSE)
            self.Close()
        dialog.Destroy()

    def OnCloseWindow(self, event):
        # message box
        style = wx.YES_NO
        title = '今日のアラーム'
        message = 'アラームの実行なしで起動しますか？'
        dialog = wx.MessageDialog(None, message, title, style=style)

        # after message
        res = dialog.ShowModal()
        if res == wx.ID_YES:
            self.Unbind(wx.EVT_CLOSE)
            self.Close()
        dialog.Destroy()
